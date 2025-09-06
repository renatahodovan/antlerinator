# Copyright (c) 2021-2025 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import sys

from os import makedirs
from os.path import abspath, dirname, isfile, join

import pytest

from setuptools.dist import Distribution
from setuptools.errors import ModuleError

import antlerinator


is_windows = sys.platform.startswith('win32')
script_ext = '.bat' if is_windows else '.sh'

tested_antlr_version = '4.13.2'
resources_dir = join(dirname(abspath(__file__)), 'resources')

try:
    Distribution().get_command_class('editable_wheel')
    has_editable_wheel = True
except ModuleError:
    has_editable_wheel = False


def test_build_antlr_providers(tmpdir):
    """
    Test whether both the ``antlerinator:`` and the ``file:`` providers work.
    Also test whether ``build_antlr`` can deal with multiple ANTLR tool
    executions.
    """
    with tmpdir.as_cwd():
        antlr_jar_path = antlerinator.download(version=tested_antlr_version, path=join(str(tmpdir), 'antlr.jar'))

        dist = Distribution({
            'name': 'pkg',
            'script_name': 'setup.py',
            'script_args': ['build_antlr'],
            'options': {
                'build_antlr': {
                    'commands': f'''
                        antlerinator:{tested_antlr_version} {join(resources_dir, "Hello.g4")} -Dlanguage=Python3 -o {tmpdir} -Xexact-output-dir
                        file:{antlr_jar_path} {join(resources_dir, "Bello.g4")} -Dlanguage=Python3 -o {tmpdir} -Xexact-output-dir
                    ''',
                },
            },
        })

        dist.parse_command_line()
        dist.run_commands()

        assert isfile('HelloLexer.py')
        assert isfile('HelloParser.py')
        assert isfile('BelloLexer.py')
        assert isfile('BelloParser.py')


def test_build_antlr_java(tmpdir):
    """
    Test whether ``build_antlr`` can deal with a custom java VM.
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'script_name': 'setup.py',
            'script_args': ['build_antlr'],
            'options': {
                'build_antlr': {
                    'commands': 'file:antlr.jar Dummy.g4',
                    'java': f'{join(resources_dir, "mock_java")}{script_ext}',
                },
            },
        })

        dist.parse_command_line()
        dist.run_commands()

        with open('mock_java_output.txt', 'r') as f:
            output = f.read()
        assert '-jar antlr.jar Dummy.g4' in output


def test_build(tmpdir):
    """
    Test whether lexer/parser generation happens when the general ``build``
    command is invoked (which is also invoked during ``install``).
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'packages': ['pkg'],
            'script_name': 'setup.py',
            'script_args': ['build', f'--build-lib={join("build", "lib")}'],  # NOTE: --build-lib is necessary to ensure that purelib build directory is used
            'options': {
                'build_antlr': {
                    'commands': f'antlerinator:{tested_antlr_version} {join(resources_dir, "Hello.g4")} -Dlanguage=Python3 -o {join(str(tmpdir), "pkg")} -Xexact-output-dir',
                },
            },
        })
        makedirs('pkg')
        with open(join('pkg', '__init__.py'), 'w'):
            pass

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('build', 'lib', 'pkg', 'HelloLexer.py'))
        assert isfile(join('build', 'lib', 'pkg', 'HelloParser.py'))


def test_develop(tmpdir):
    """
    Test whether lexer/parser generation happens for editable installs (via
    development mode).
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'packages': ['pkg'],
            'script_name': 'setup.py',
            'script_args': ['develop'],
            'options': {
                'build_antlr': {
                    'commands': f'antlerinator:{tested_antlr_version} {join(resources_dir, "Hello.g4")} -Dlanguage=Python3 -o {join(str(tmpdir), "pkg")} -Xexact-output-dir',
                },
            },
        })
        makedirs('pkg')
        with open(join('pkg', '__init__.py'), 'w'):
            pass
        with open('setup.py', 'w') as f:
            f.write('from setuptools import setup; setup(name="pkg", packages=["pkg"])')

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('pkg', 'HelloLexer.py'))
        assert isfile(join('pkg', 'HelloParser.py'))


@pytest.mark.skipif(not has_editable_wheel, reason='editable_wheel command unavailable')
def test_editable_wheel(tmpdir):
    """
    Test whether lexer/parser generation happens for editable installs (via
    editable wheels).
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'packages': ['pkg'],
            'script_name': 'setup.py',
            'script_args': ['editable_wheel'],
            'options': {
                'build_antlr': {
                    'commands': f'antlerinator:{tested_antlr_version} {join(resources_dir, "Hello.g4")} -Dlanguage=Python3 -o {join(str(tmpdir), "pkg")} -Xexact-output-dir',
                },
            },
        })
        makedirs('pkg')
        with open(join('pkg', '__init__.py'), 'w'):
            pass

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('pkg', 'HelloLexer.py'))
        assert isfile(join('pkg', 'HelloParser.py'))


def test_clean(tmpdir):
    """
    Test whether cleanup removes generated files.
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'packages': ['pkg'],
            'script_name': 'setup.py',
            'script_args': ['clean'],
            'options': {
                'build_antlr': {
                    'output': join('pkg', 'Dummy*.py'),
                },
            },
        })
        makedirs('pkg')
        with open(join('pkg', '__init__.py'), 'w'):
            pass
        with open(join('pkg', 'DummyLexer.py'), 'w'):
            pass
        with open(join('pkg', 'DummyParser.py'), 'w'):
            pass

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('pkg', '__init__.py'))
        assert not isfile(join('pkg', 'DummyLexer.py'))
        assert not isfile(join('pkg', 'DummyParser.py'))


def test_sdist(tmpdir):
    """
    Test whether generated files can be excluded from the sdist using
    MANIFEST.in.
    """
    with tmpdir.as_cwd():
        dist = Distribution({
            'name': 'pkg',
            'packages': ['pkg'],
            'script_name': 'setup.py',
            'options': {
                'build_antlr': {
                    'output': join('pkg', 'Dummy*.py'),
                },
            },
        })
        makedirs('pkg')
        with open(join('pkg', '__init__.py'), 'w'):
            pass
        with open(join('pkg', 'DummyLexer.py'), 'w'):
            pass
        with open(join('pkg', 'DummyParser.py'), 'w'):
            pass
        with open('MANIFEST.in', 'w') as f:
            f.write('exclude pkg/Dummy*.py')

        sdist = dist.get_command_class('sdist')
        cmd = sdist(dist)
        cmd.ensure_finalized()
        cmd.run()

        manifest = cmd.filelist.files
        assert join('pkg', '__init__.py') in manifest
        assert join('pkg', 'DummyLexer.py') not in manifest
        assert join('pkg', 'DummyParser.py') not in manifest
