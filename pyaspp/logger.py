import sys

def _print(stream, *what):
    acc = ''
    for w in what:
        acc += str(w)
    stream.write(acc + '\n')

def warn(*what):
    _print(sys.stderr, 'warn: ', *what)

def log(*what):
    _print(sys.stdout, *what)
