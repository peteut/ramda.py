import collections

def eq(a, b):
    if all(map(lambda arg: isinstance(arg, collections.Iterable), [a, b])):
        return all(map(lambda args: args[0] == args[1], zip(a, b)))
    assert a == b
