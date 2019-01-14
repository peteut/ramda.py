from .internal import _curry1, _curry2, _keys, _contains, _is_object, \
    _is_array, _is_string


__all__ = ["keys", "omit", "prop", "pick_by", "path"]


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
    try:
        return obj.get(p, None) if _is_object(obj) else \
            obj[p] if _is_array(obj) else getattr(obj, p, None)
    except IndexError:
        pass


@_curry2
def pick_by(test, obj):
    result = {}
    for key, value in obj.items():
        if test(value, key, obj) is not False:
            result[key] = value
    return result


@_curry2
def path(paths, obj):
    val = obj
    for key in paths:
        if not val:
            return

        val = prop(key, val)

    return val
