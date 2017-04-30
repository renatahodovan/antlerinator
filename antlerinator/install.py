# Copyright (c) 2017 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import errno
import json
import pkgutil
import urllib.request

from argparse import ArgumentParser
from os import makedirs
from os.path import dirname, exists, expanduser, join


config = json.loads(pkgutil.get_data(__package__, 'config.json').decode('ascii'))
__version__ = config['version']
antlr_jar_path = join(expanduser('~'), '.antlerinator', config['tool_name'])


def install(*, force=False, lazy=False):
    """
    Download the ANTLR v4 tool jar. (Raises :exception:`FileExistsError` if jar
    is already available, unless ``lazy`` is ``True``.)

    :param bool force: Force download even if local jar already exists.
    :param bool lazy: Don't report an error if local jar already exists and
        don't try to download it either.
    """

    if exists(antlr_jar_path):
        if lazy:
            return
        if not force:
            raise FileExistsError(errno.EEXIST, 'file already exists', antlr_jar_path)

    tool_url = config['tool_url']
    with urllib.request.urlopen(tool_url) as response:
        tool_jar = response.read()

    makedirs(dirname(antlr_jar_path), exist_ok=True)

    with open(antlr_jar_path, mode='wb') as tool_file:
        tool_file.write(tool_jar)


def execute():
    """
    Entry point of the install helper tool to ease the download of the right
    version of the ANTLR v4 tool jar.
    """

    arg_parser = ArgumentParser(description='Install helper tool to download the right version of the ANTLR v4 tool jar.')

    arg_parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    mode_group = arg_parser.add_mutually_exclusive_group()
    mode_group.add_argument('-f', '--force', action='store_true', default=False,
                            help='force download even if local antlr4.jar already exists')
    mode_group.add_argument('-l', '--lazy', action='store_true', default=False,
                            help='don\'t report an error if local antlr4.jar already exists and don\'t try to download it either')

    args = arg_parser.parse_args()

    install(force=args.force, lazy=args.lazy)


if __name__ == '__main__':
    execute()
