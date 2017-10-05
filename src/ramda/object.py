from .internal import _curry1, _curry2, _keys, _contains


__all__ = ["keys", "omit", "prop"]


keys = _curry1(_keys)


@_curry2
def omit(names, obj):
    result = {}
    for key in obj.keys():
        if not _contains(key, names):
            result[key] = obj[key]
    return result


@_curry2
def prop(p, obj):
    return obj[p]
