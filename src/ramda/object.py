import collections
from .internal import _curry1


__all__ = ["keys"]


@_curry1
def keys(obj):
    return obj.keys() if isinstance(obj, collections.Mapping) else \
        [idx for idx in range(len(obj))] if isinstance(obj, collections.Sequence) else \
        []
