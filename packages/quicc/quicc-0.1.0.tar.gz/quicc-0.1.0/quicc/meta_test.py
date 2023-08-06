
# Copyright 2019-, Gavin E. Crooks and contributors
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

import io
import glob
import subprocess

import quicc as qc
from quicc import meta


def test_version():
    assert qc.__version__


def test_print_requirements():
    out = io.StringIO()
    meta.print_requirements(out)
    print(out)


def test_print_requirements_main():
    rval = subprocess.call(['python', '-m', 'quicc.meta'])
    assert rval == 0


def test_copyright():
    """Check that source code files contain a copyright line"""
    exclude = set(['quicc/version.py'])
    for fname in glob.glob('quicc/**/*.py', recursive=True):
        if fname in exclude:
            continue
        print("Checking " + fname + " for copyright header")

        with open(fname) as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                assert line.startswith('# Copyright')
                break
