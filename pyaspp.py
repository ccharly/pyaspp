#!/usr/bin/env python

import sys
import argparse

from pyaspp.pp import pypp
from pyaspp.pp import cpp

def _description():
    return 'A C preprocessor that interprets python'

""" The usage

    We do override the usage since the one given by `argparse` put the positional
    arguments at the end of it.
"""
def _usage():
    return 'usage: pyaspp.py [-h] FILES ... --then THEN [THEN ...]'

def _parse_opts(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=_description(), usage=_usage())
    parser.add_argument('files', nargs='+')
    parser.add_argument('--then', dest='then', nargs='+')
    return parser.parse_args(args)

def pyaspp():
    opts = _parse_opts()
    for f in opts.files:
        try:
            pypp.pp_file(f)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)


if __name__ == "__main__":
    pyaspp()
