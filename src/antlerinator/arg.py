# Copyright (c) 2021-2022 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from inators.arg import add_argument

from .download import __antlr_version__, default_antlr_jar_path, download


def add_antlr_argument(
        parser,
        short_alias=(),
        long_alias=(),
        *,
        metavar='FILE',
        help=f'path of the ANTLR v4 tool jar file (default: {default_antlr_jar_path(__antlr_version__ or "VERSION")})'
):
    """
    add_antlr_argument(parser, short_alias=(), long_alias=(), *, metavar='FILE', help='path of the ANTLR v4 tool jar file (default:  ~/.antlerinator/antlr-VERSION-complete.jar)')

    Add an ``--antlr`` command-line argument to ``parser``.

    The default processing of the added argument is implemented in
    :func:`process_antlr_argument`.

    :param ~argparse.ArgumentParser parser: The parser to add the argument to.
    :param short_alias: Add short flag alias(es) for ``--antlr``.
    :type short_alias: str or list(str) or tuple(str)
    :param long_alias: Add long option alias(es) for ``--antlr``.
    :type long_alias: str or list(str) or tuple(str)
    :param str metavar: Override the default argument name in usage messages.
    :param str help: Override the default description of ``--antlr``.

    .. argdoc {'help': 'path of the ANTLR v4 tool jar file (default:  ~/.antlerinator/antlr-VERSION-complete.jar)'}
    """
    # NOTE: The first line of the docstring (i.e., the documented signature)
    #   must be kept in sync with the actual signature of the function!

    add_argument(parser, short_alias, '--antlr', long_alias,
                 metavar=metavar, default=None, help=help)


def process_antlr_argument(args):
    """
    Lazily download the ANTLR v4 tool jar to the default path if ``--antlr`` was
    *not* given on the command line. I.e., download and copy the jar to the
    default path if it is not already there (using
    :func:`antlerinator.download`). Also set ``args.antlr`` to the path to the
    jar. No-op if ``--antlr`` was specified on the command line.

    This implements the default processing of the ``--antlr`` command-line
    argument added by :func:`add_antlr_argument`.

    :param args: A namespace object populated by
        :meth:`argparse.ArgumentParser.parse_args`.
    """

    if not args.antlr:
        args.antlr = download(lazy=True)
