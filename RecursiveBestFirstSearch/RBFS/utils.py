import functools

# This function is used to memoize the results of a function, so that if the same input is given, the function will return the same output. In this case, we will be using it to get the heuristic values of the nodes of the map
def memoize(function, slot=None, maxsize=32):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = function(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return function(*args)

    return memoized_fn