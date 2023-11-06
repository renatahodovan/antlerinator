# Copyright (c) 2017-2023 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import os
import subprocess
import sys

import pytest

import antlerinator


def run_antlr(jar_path):
    cmd = ('java', '-jar', jar_path)
    subprocess.run(cmd, check=True)


def run_download(args, exp_ok):
    cmd = (sys.executable, '-m', 'antlerinator') + args

    returncode = subprocess.run(cmd, check=False).returncode

    if exp_ok:
        assert returncode == 0
    else:
        assert returncode != 0


@pytest.mark.parametrize('antlr_version', [
    '4.6',  # the first ANTLR version that was supported by ANTLeRinator epoch 0
    # '4.7',
    # '4.7.1',
    # '4.7.2',
    # '4.8',
    # '4.9',
    # '4.9.1',
    '4.9.2',  # the last ANTLR version that was supported by ANTLeRinator epoch 0
])
@pytest.mark.parametrize('default_path', [
    True,
    False
])
class TestDownload:

    def test_cli(self, antlr_version, default_path, tmpdir):
        args = [f'--antlr-version={antlr_version}']

        if not default_path:
            jar_path = os.path.join(str(tmpdir), 'antlr4.jar')
            args += [f'--output={jar_path}']
        else:
            jar_path = antlerinator.default_antlr_jar_path(antlr_version)

        run_download(args=tuple(args) + ('--force', ), exp_ok=True)
        run_download(args=tuple(args) + ('--lazy', ), exp_ok=True)
        run_download(args=tuple(args), exp_ok=False)
        run_antlr(jar_path)

    def test_api(self, antlr_version, default_path, tmpdir):
        kwargs = {'version': antlr_version}

        if not default_path:
            kwargs['path'] = os.path.join(str(tmpdir), 'antlr4.jar')

        jar_path_force = antlerinator.download(force=True, **kwargs)
        jar_path_lazy = antlerinator.download(lazy=True, **kwargs)
        with pytest.raises(OSError):
            antlerinator.download(**kwargs)
        assert jar_path_force == jar_path_lazy
        run_antlr(jar_path_force)
