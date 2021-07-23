# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest
import sys

from os import makedirs
from os.path import abspath, dirname, isfile, join
from setuptools.dist import Distribution

import antlerinator


is_windows = sys.platform.startswith('win32')
script_ext = '.bat' if is_windows else '.sh'

tested_antlr_version = '4.9.2'
resources_dir = join(dirname(abspath(__file__)), 'resources')


def test_build_antlr_providers(tmpdir):
    """
    Test whether both the ``antlerinator:`` and the ``file:`` providers work.
    Also test whether ``build_antlr`` can deal with multiple ANTLR tool
    executions.
    """
    with tmpdir.as_cwd():
        antlr_jar_path = antlerinator.download(version=tested_antlr_version, path=join(str(tmpdir), 'antlr.jar'))

        dist = Distribution(dict(
            name='pkg',
            script_name='setup.py',
            script_args=['build_antlr'],
            options=dict(
                build_antlr=dict(
                    commands='''
                        antlerinator:{tested_antlr_version} {grammar1} -Dlanguage=Python3 -o {tmpdir} -Xexact-output-dir
                        file:{antlr_jar_path} {grammar2} -Dlanguage=Python3 -o {tmpdir} -Xexact-output-dir
                    '''.format(
                        tested_antlr_version=tested_antlr_version,
                        antlr_jar_path=antlr_jar_path,
                        grammar1=join(resources_dir, 'Hello.g4'),
                        grammar2=join(resources_dir, 'Bello.g4'),
                        tmpdir=tmpdir,
                    ),
                ),
            ),
        ))

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
        dist = Distribution(dict(
            name='pkg',
            script_name='setup.py',
            script_args=['build_antlr'],
            options=dict(
                build_antlr=dict(
                    commands='file:antlr.jar Dummy.g4',
                    java=join(resources_dir, 'mock_java') + script_ext,
                ),
            ),
        ))

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
        dist = Distribution(dict(
            name='pkg',
            packages=['pkg'],
            script_name='setup.py',
            script_args=['build', '--build-lib={buildlib}'.format(buildlib=join('build', 'lib'))],  # NOTE: --build-lib is necessary to ensure that purelib build directory is used
            options=dict(
                build_antlr=dict(
                    commands='antlerinator:{tested_antlr_version} {grammar} -Dlanguage=Python3 -o {pkgdir} -Xexact-output-dir'.format(
                        tested_antlr_version=tested_antlr_version,
                        grammar=join(resources_dir, 'Hello.g4'),
                        pkgdir=join(str(tmpdir), 'pkg'),
                    ),
                ),
            ),
        ))
        makedirs('pkg')
        open(join('pkg', '__init__.py'), 'w').close()

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('build', 'lib', 'pkg', 'HelloLexer.py'))
        assert isfile(join('build', 'lib', 'pkg', 'HelloParser.py'))


def test_develop(tmpdir):
    """
    Test whether lexer/parser generation happens for editable installs.
    """
    with tmpdir.as_cwd():
        dist = Distribution(dict(
            name='pkg',
            packages=['pkg'],
            script_name='setup.py',
            script_args=['develop'],
            options=dict(
                build_antlr=dict(
                    commands='antlerinator:{tested_antlr_version} {grammar} -Dlanguage=Python3 -o {pkgdir} -Xexact-output-dir'.format(
                        tested_antlr_version=tested_antlr_version,
                        grammar=join(resources_dir, 'Hello.g4'),
                        pkgdir=join(str(tmpdir), 'pkg'),
                    ),
                ),
            ),
        ))
        makedirs('pkg')
        open(join('pkg', '__init__.py'), 'w').close()

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('pkg', 'HelloLexer.py'))
        assert isfile(join('pkg', 'HelloParser.py'))


def test_clean(tmpdir):
    """
    Test whether cleanup removes generated files.
    """
    with tmpdir.as_cwd():
        dist = Distribution(dict(
            name='pkg',
            packages=['pkg'],
            script_name='setup.py',
            script_args=['clean'],
            options=dict(
                build_antlr=dict(
                    output=join('pkg', 'Dummy*.py'),
                ),
            ),
        ))
        makedirs('pkg')
        open(join('pkg', '__init__.py'), 'w').close()
        open(join('pkg', 'DummyLexer.py'), 'w').close()
        open(join('pkg', 'DummyParser.py'), 'w').close()

        dist.parse_command_line()
        dist.run_commands()

        assert isfile(join('pkg', '__init__.py'))
        assert not isfile(join('pkg', 'DummyLexer.py'))
        assert not isfile(join('pkg', 'DummyParser.py'))


def test_sdist(tmpdir):
    """
    Test whether generated files are cleaned before creating an sdist.
    """
    with tmpdir.as_cwd():
        dist = Distribution(dict(
            name='pkg',
            packages=['pkg'],
            script_name='setup.py',
            options=dict(
                build_antlr=dict(
                    output=join('pkg', 'Dummy*.py'),
                ),
            ),
        ))
        makedirs('pkg')
        open(join('pkg', '__init__.py'), 'w').close()
        open(join('pkg', 'DummyLexer.py'), 'w').close()
        open(join('pkg', 'DummyParser.py'), 'w').close()

        sdist = dist.get_command_class('sdist')
        cmd = sdist(dist)
        cmd.ensure_finalized()
        cmd.run()

        manifest = cmd.filelist.files
        assert join('pkg', '__init__.py') in manifest
        assert join('pkg', 'DummyLexer.py') not in manifest
        assert join('pkg', 'DummyParser.py') not in manifest
