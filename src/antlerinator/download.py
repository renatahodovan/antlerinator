# Copyright (c) 2017-2024 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import contextlib
import errno
import ssl

from argparse import ArgumentParser
from importlib import metadata
from os import makedirs
from os.path import basename, dirname, exists, expanduser, join
from urllib.request import urlopen

import inators


__version__ = metadata.version(__package__)

try:
    __antlr_version__ = metadata.version('antlr4-python3-runtime')
except metadata.PackageNotFoundError:
    __antlr_version__ = None


def default_antlr_jar_path(version=None):
    """
    Default path to download the ANTLR v4 tool jar to.

    :param str version: The version of ANTLR v4. If ``None``, it defaults to the
        version of the installed antlr4 runtime package (unless the package is
        not installed, in which case a :exc:`ValueError` is raised).
    :return: The version-specific default path.
    """
    version = version or __antlr_version__
    if not version:
        raise ValueError('version must be specified if antlr4 runtime is not installed')
    return join(expanduser('~'), '.antlerinator', f'antlr-{version}-complete.jar')


def download(version=None, path=None, *, force=False, lazy=False):
    """
    Download the ANTLR v4 tool jar. (Raises :exc:`OSError` if jar is already
    available, unless ``lazy`` is ``True``.)

    :param str version: The version of ANTLR v4 tool jar to download. If
        ``None``, it defaults to the version of the installed antlr4 runtime
        package (unless the package is not installed, in which case a
        :exc:`ValueError` is raised).
    :param str path: Path to save the downloaded jar to. If ``None``, it
        defaults to ``default_antlr_jar_path(version)``.
    :param bool force: Force download even if jar already exists at path.
    :param bool lazy: Don't report an error if jar already exists at path and
        don't try to download it either.
    :return: Path to the downloaded jar.
    """

    default_tool_path = default_antlr_jar_path(version)
    tool_path = path or default_tool_path
    tool_url = f'https://www.antlr.org/download/{basename(default_tool_path)}'

    if exists(tool_path):
        if lazy:
            return tool_path
        if not force:
            raise OSError(errno.EEXIST, 'file already exists', tool_path)

    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    with contextlib.closing(urlopen(tool_url, context=ssl_context)) as response:
        tool_bytes = response.read()

    tool_dir = dirname(tool_path)
    makedirs(tool_dir, exist_ok=True)

    with open(tool_path, mode='wb') as tool_file:
        tool_file.write(tool_bytes)

    return tool_path


def execute():
    """
    Entry point of the download helper tool that eases getting the right
    version of the ANTLR v4 tool jar.
    """

    arg_parser = ArgumentParser(description='Download helper tool to get the right version of the ANTLR v4 tool jar.')

    arg_parser.add_argument('--antlr-version', metavar='VERSION', default=__antlr_version__,
                            help='version of ANTLR v4 tool jar to download (default: %(default)s)')
    arg_parser.add_argument('--output', metavar='FILE', default=None,
                            help=f'path to save the downloaded jar to (default: {default_antlr_jar_path("VERSION").replace(expanduser("~"), "~")})')

    mode_group = arg_parser.add_mutually_exclusive_group()
    mode_group.add_argument('--force', action='store_true', default=False,
                            help='force download even if jar already exists at the output path')
    mode_group.add_argument('--lazy', action='store_true', default=False,
                            help='don\'t report an error if jar already exists at the output path and don\'t try to download it either')

    inators.arg.add_version_argument(arg_parser, version=__version__)

    args = arg_parser.parse_args()

    download(version=args.antlr_version, path=args.output, force=args.force, lazy=args.lazy)
