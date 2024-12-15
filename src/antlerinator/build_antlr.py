# Copyright (c) 2021-2024 Renata Hodovan, Akos Kiss.
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

from setuptools import Command
from setuptools.errors import ModuleError, OptionError

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
            raise OptionError(f"'commands' must be a list of strings or tuples (got {commands!r})")

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
                    raise OptionError(f"strings in 'commands' must start with a 'provider:arg' pattern (got {cmd!r})")
                provider, provider_arg, antlr_args = m.group('provider', 'provider_arg', 'antlr_args')

                provider = providers.get(provider)
                if not provider:
                    raise OptionError(f"unknown provider in 'commands' (options: {', '.join(providers.keys())}; got: {provider})")
                antlr_args = tuple(shlex.split(antlr_args, posix=posix))

                cmd = (provider, provider_arg, antlr_args)

            if isinstance(cmd, tuple):
                if len(cmd) != 3:
                    raise OptionError(f"tuples in 'commands' must be 3-tuples (got {cmd!r})")
            else:
                raise OptionError(f"elements in 'commands' must be strings or tuples (got {commands!r})")

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
        files = [f for o in output for f in glob.glob(o, recursive=True)]
        for f in files:
            self.execute(os.unlink, (f,))


def register(dist):

    build = dist.get_command_class('build')
    develop = dist.get_command_class('develop')
    clean = dist.get_command_class('clean')

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

    dist.cmdclass['build'] = antlerinator_build
    dist.cmdclass['develop'] = antlerinator_develop
    dist.cmdclass['clean'] = antlerinator_clean

    # Patch editable_wheel only if available
    try:
        editable_wheel = dist.get_command_class('editable_wheel')

        class antlerinator_editable_wheel(editable_wheel):
            def run(self):
                self.run_command('build_antlr')
                editable_wheel.run(self)

        dist.cmdclass['editable_wheel'] = antlerinator_editable_wheel
    except ModuleError:
        pass
