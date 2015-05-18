#!/usr/bin/env python

import sys
import argparse

def _description():
    return 'A C preprocessor that interprets python'

""" The usage

    We do override the usage since the one given by `argparse` put the positional
    arguments at the end of it.
"""
def _usage():
    return 'usage: pyp2c.py [-h] FILES ... --then THEN [THEN ...]'

def _parse_opts(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=_description(), usage=_usage())
    parser.add_argument('files', nargs='+')
    parser.add_argument('--then', dest='then', nargs='+', required=True)
    return vars(parser.parse_args(args))

def pyp2c():
    opts = _parse_opts()
    print(opts)
    pass

if __name__ == "__main__":
    pyp2c()
