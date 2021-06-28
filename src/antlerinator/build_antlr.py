# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import glob
import os
import re
import shlex
import sys

from distutils.errors import DistutilsOptionError
from setuptools import Command

from .download import download


class build_antlr(Command):

    description = 'build (generate) parsers/lexers from ANTLR v4 grammar files'

    user_options = [
        ('commands=', None, 'list of antlr4 invocations'),
        ('output=', None, 'list of file names or glob patterns that are the result of commands'),
        ('java=', None, 'path to java'),
    ]

    def initialize_options(self):
        self.commands = None
        self.output = None
        self.java = None

    def finalize_options(self):
        # parse 'commands' option
        commands = self.commands or []

        if isinstance(commands, str):
            if '\n' in commands:
                commands = commands.splitlines()
            else:
                commands = commands.split(',')
            commands = [cmd.strip() for cmd in commands if cmd.strip()]

        if not isinstance(commands, list):
            raise DistutilsOptionError("'commands' must be a list of strings or tuples (got %r)" % commands)

        cmd_re = re.compile('^(?P<provider>^[^\\d\\W]\\w*):(?P<provider_arg>\\S*)\\s+(?P<antlr_args>.*)$')
        providers = {
            'file': lambda arg: arg,
            'antlerinator': lambda arg: download(arg, lazy=True),
        }
        posix = sys.platform != 'win32'

        for i, cmd in enumerate(commands):
            if isinstance(cmd, str):
                m = cmd_re.match(cmd)
                if not m:
                    raise DistutilsOptionError("strings in 'commands' must start with a 'provider:arg' pattern (got %r)" % cmd)
                provider, provider_arg, antlr_args = m.group('provider', 'provider_arg', 'antlr_args')

                provider = providers.get(provider)
                if not provider:
                    raise DistutilsOptionError("unknown provider in 'commands' (options: %s; got: %s)" % (', '.join(providers.keys()), provider))
                antlr_args = tuple(shlex.split(antlr_args, posix=posix))

                cmd = (provider, provider_arg, antlr_args)

            if isinstance(cmd, tuple):
                if len(cmd) != 3:
                    raise DistutilsOptionError("tuples in 'commands' must be 3-tuples (got %r)" % cmd)
            else:
                raise DistutilsOptionError("elements in 'commands' must be strings or tuples (got %r)" % commands)

            commands[i] = cmd

        self.commands = commands

        # process 'output' option
        self.ensure_string_list('output')
        if self.output is None:
            self.output = []

        # ensure default for 'java' option
        if not self.java:
            self.java = 'java'

    def run(self):
        for provider, provider_arg, antlr_args in self.commands:
            self.spawn([self.java, '-jar', provider(provider_arg)] + list(antlr_args))


class clean_antlr(Command):

    description = 'clean parsers/lexers generated from ANTLR v4 grammar files'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        output = self.get_finalized_command('build_antlr').output
        files = [f for o in output for f in glob.glob(o)]  # NOTE: glob(,recursive=True) omitted because of py2
        for f in files:
            self.execute(os.unlink, (f,))


def register(dist):

    build = dist.get_command_class('build')
    develop = dist.get_command_class('develop')
    clean = dist.get_command_class('clean')
    sdist = dist.get_command_class('sdist')

    class antlerinator_build(build):
        def run(self):
            self.run_command('build_antlr')
            build.run(self)

    class antlerinator_develop(develop):
        def run(self):
            self.run_command('build_antlr')
            develop.run(self)

    class antlerinator_clean(clean):
        def run(self):
            self.run_command('clean_antlr')
            clean.run(self)

    class antlerinator_sdist(sdist):
        def run(self):
            self.run_command('clean_antlr')
            sdist.run(self)

    dist.cmdclass['build'] = antlerinator_build
    dist.cmdclass['develop'] = antlerinator_develop
    dist.cmdclass['clean'] = antlerinator_clean
    dist.cmdclass['sdist'] = antlerinator_sdist
