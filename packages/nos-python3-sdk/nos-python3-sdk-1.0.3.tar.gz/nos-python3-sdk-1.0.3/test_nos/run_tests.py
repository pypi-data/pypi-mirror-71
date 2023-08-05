#!/usr/bin/env python
# -*- coding:utf8 -*-



import sys
import atexit
from os.path import dirname, abspath

import nose


def run_all(argv=None):
    atexit.register(lambda: sys.stderr.write('Shutting down....\n'))

    # always insert coverage when running tests
    if argv is None:
        argv = [
            'nosetests', '--with-xunit',
            '--with-xcoverage', '--cover-package=nos',
            '--cover-erase', '--cover-branches',
            '--logging-filter=nos', '--logging-level=DEBUG',
            '--verbose'
        ]

    nose.run_exit(
        argv=argv,
        defaultTest=abspath(dirname(__file__))
    )

if __name__ == '__main__':
    run_all(sys.argv)
