import re

directive_re = re.compile('^#py.* ')

class Context(object):
    """ Context """

    filename = None
    globalz = {}

    def __init__(self, filename):
        self.filename = filename
        self.exec_stmt('import sys, os')
        self.exec_stmt('_PYASPP_ROOT = os.path.abspath(os.path.dirname(sys.argv[0]))')
        self.eval_expr('sys.path.append(_PYASPP_ROOT + "/pyaspp/pp" )')
        self.exec_stmt('import cpp')

    def eval_expr(self, expr):
        return eval(expr, self.globalz)

    def exec_stmt(self, stmt):
        exec(stmt, self.globalz)

def eval_expr(ctx, expr):
    ret = ctx.eval_expr(expr)
    if hasattr(ret, '__str__'):
        print(str(ret))

_kind_pattern = '#py.' # '.' mean everything
_kind_pattern_len = len(_kind_pattern)

_kinds_tbl = {
        '=': eval_expr
}

def _is_directive(line):
    return directive_re.match(line)

def _has_kind(prefix):
    return len(prefix) == _kind_pattern_len

def _get_kind(prefix):
    kind = prefix[_kind_pattern_len - 1]
    return kind if kind in _kinds_tbl else None

def make_context(filename, inherits_from=None):
    return Context(filename)

def pp_line(ctx, line):
    if _is_directive(line):
        prefix, line = tuple(line.split(' ', 1))
        if _has_kind(prefix):
            kind = _get_kind(prefix)
            if kind is None:
                print("-- Invalid kind for #py directive")
            else:
                _kinds_tbl[kind](ctx, line)
        else:
            ctx.exec_stmt(line);
    else:
        print(line)

def pp_file(filename):
    ctx = make_context(filename)
    with open(filename, 'r') as f:
        for line in f:
            pp_line(ctx, line.replace('\n', ''))
