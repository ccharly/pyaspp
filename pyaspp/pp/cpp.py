
or_ = "||"
and_ = "&&"

def defined(v):
    return "defined({})".format(v)

def define(lhs, rhs=None):
    return "#define {} {}".format(lhs, rhs if not None else "")
