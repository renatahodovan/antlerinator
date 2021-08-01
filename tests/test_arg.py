# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import argparse
import pytest

import antlerinator


@pytest.mark.parametrize('func_args, func_kwargs, sys_argv, exp', [
    ([], {}, [], None),
    ([], {}, ['--antlr', './antlr.jar'], './antlr.jar'),
    (['-A'], {}, ['-A', './antlr.jar'], './antlr.jar'),
    ([(), '--antlr:antlr'], {}, ['--antlr:antlr', './antlr.jar'], './antlr.jar'),
    ([], {'short_alias': '-A'}, ['-A', './antlr.jar'], './antlr.jar'),
    ([], {'long_alias': '--antlr:antlr'}, ['--antlr:antlr', './antlr.jar'], './antlr.jar'),
])
def test_add_antlr_argument(func_args, func_kwargs, sys_argv, exp):
    parser = argparse.ArgumentParser()
    antlerinator.add_antlr_argument(parser, *func_args, **func_kwargs)
    args = parser.parse_args(sys_argv)
    assert args.antlr == exp
