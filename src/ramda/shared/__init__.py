from ..internal import _is_seq


def eq(a, b):
    if all(map(lambda arg: _is_seq(arg), [a, b])):
        return all(map(lambda args: args[0] == args[1], zip(a, b)))
    assert a == b
