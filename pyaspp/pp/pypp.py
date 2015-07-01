import re
import os
import types
import bunch
from .. import logger

class PPError(Exception):
    pass

directive_re = re.compile('^#py.')

class Context(object):
    """ Context """

    globalz = {}
    loc = bunch.Bunch()

    def __init__(self, filename):
        self.exec_stmt('import sys, os')
        self.exec_stmt('_PYASPP_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))')
        self.eval_expr('sys.path.append(_PYASPP_ROOT + "/pyaspp/pp" )')
        self.exec_stmt('import cpp')
        self.loc.line = 1
        self.loc.filename = filename

    def eval_expr(self, expr):
        return eval(expr, self.globalz)

    def exec_stmt(self, stmt):
        exec(stmt, self.globalz)

_py_block = []
_in_py_block = False

def exec_stmt(ctx, stmt):
    ctx.exec_stmt(stmt.lstrip())

def eval_expr(ctx, expr):
    ret = ctx.eval_expr(expr)
    if ret is None:
        return
    if isinstance(ret, types.GeneratorType):
        for step in ret:
            print(str(step))
    elif hasattr(ret, '__str__'):
        print(str(ret))

def begin_block(ctx, expr):
    global _in_py_block
    if _in_py_block:
        raise PPError('nested py block are not allowed!')
    _in_py_block = True
    _py_block = []

def end_block(ctx, expr):
    global _in_py_block
    if not _in_py_block:
        raise PPError('closing a non-opened py block!')
    _in_py_block = False
    ctx.exec_stmt('\n'.join(_py_block))

_kind_pattern = '#py.' # '.' mean everything
_kind_pattern_len = len(_kind_pattern)

_kinds_tbl = {
        '=': eval_expr,
        '{': begin_block,
        '}': end_block,
}

def _is_directive(line):
    return directive_re.match(line)

def _has_kind(prefix):
    return len(prefix) == _kind_pattern_len

def _get_kind(prefix):
    kind = prefix[_kind_pattern_len - 1]
    return kind if kind in _kinds_tbl else None

def print_loc(ctx, plus=0):
    loc = ctx.loc.line + plus
    print('#line {} "{}"'.format(loc, ctx.loc.filename))

def make_context(filename, inherits_from=None):
    return Context(filename)

def pp_line(ctx, line):
    global _in_py_block
    if _is_directive(line):
        prefix, line = tuple(line.split(' ', 1))
        if _has_kind(prefix):
            kind = _get_kind(prefix)
            if kind is None:
                raise PPError("invalid kind for #py directive!")
            else:
                kind_fun = _kinds_tbl[kind]
                if _in_py_block and kind_fun != end_block:
                    raise PPError('py directives are not allowed in py block!')
                if kind_fun == begin_block:
                    print_loc(ctx)
                    kind_fun(ctx, line)
                elif kind_fun == end_block:
                    kind_fun(ctx, line)
                    print_loc(ctx, 1)
                else:
                    print_loc(ctx)
                    kind_fun(ctx, line)
                    print_loc(ctx, 1)
        else:
            exec_stmt(ctx, line);
    else:
        if _in_py_block:
            _py_block.append(line)
        else:
            print(line)

def pp_file(filename):
    ctx = make_context(filename)
    with open(filename, 'r') as f:
        for line in f:
            pp_line(ctx, line.replace('\n', ' ')) # replace '\n' to ' ' so that the line.split will work
            ctx.loc.line += 1
