# Copyright (c) 2017-2019 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest
import subprocess
import sys

import antlerinator


def run_antlr():
    cmd = ('java', '-jar', antlerinator.antlr_jar_path)
    proc = subprocess.Popen(cmd)
    proc.communicate()
    assert proc.returncode == 0


def run_install(args, exp_ok):
    cmd = (sys.executable, '-m', 'antlerinator.install') + args

    proc = subprocess.Popen(cmd)
    proc.communicate()

    if exp_ok:
        assert proc.returncode == 0
    else:
        assert proc.returncode != 0


def test_cli():
    run_install(args=('--force', ), exp_ok=True)
    run_install(args=('--lazy', ), exp_ok=True)
    run_install(args=(), exp_ok=False)
    run_antlr()


def test_api():
    antlerinator.install(force=True)
    antlerinator.install(lazy=True)
    with pytest.raises(OSError):
        antlerinator.install()
    run_antlr()
