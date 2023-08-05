"""
Function decorator caching on disk the result of a function call.

The decorated function is executed and its result is stored on disk.
Later invocations of the function won't execute it, but just load
its result from disk.

Example:

@cache("foo-result.pickle")
def foo(args):
    ...
    return result
    
"""

__version__ = "0.3"
__author__ = "Pietro Spadaccino"



import os
import pickle
import functools


def cache(fpath, arg_check=False, enabled=True):
    """
    Decorator caching on file `fpath` the result of a function using pickle.

    Args:
        enabled (bool): if False the caching has no effect and the function
            is executed normally. Defaults to True.
        arg_check (bool): If True, when loading the cached result arguments
            passed to the function that produced the cached result are compared
            to arguments of the current inocation. If they are not the same
            then the cached result is not loaded and the function is executed.

    Example:
        @cache("foo-result.pickle")
        def foo_decorated(args):
            ...
            return result

    Dynamically disable of caching can't be done with `enabled` argument,
    since it can be only set once when decorating the function.
    To make enabling/disabling possible at runtime, the decorated function
    exposes an additional keyword argument named "pklcache_enable" which
    can be set to True/False to enable/disable caching.

    Example:
        foo_decorated(42, ...)   #cached
        foo_decorated(42, ..., pklcache_enable=False)  #not cached

    If "pklcache_enable" kwarg is used, it is removed from kwargs before
    calling the function, to not alter its semantics.
    """

    MAGIC = "PKLCACHE-whocaresabouttypes"
    FUNC_ENABLE_KWARG = "pklcache_enable"

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Decorated functions accept an additional kwarg to enable/disable the
            # caching dynamically. Otherwise the enabling/disabling is only possible
            # via the `enabled` argument of `cache`, which once set cannot be modified.
            # This dynamic enable has priority over static enable
            dynamic_set = False
            if FUNC_ENABLE_KWARG in kwargs:
                dynamic_set = True
                dynamic_enable = bool(kwargs[FUNC_ENABLE_KWARG])
                del kwargs[FUNC_ENABLE_KWARG]

            # If not enabled execute func and return
            if (dynamic_set and not dynamic_enable) or (not dynamic_set and not enabled):
                return func(*args, **kwargs)

            # Check if cache file is present. If yes load its contents
            if os.path.isfile(fpath):
                cached = pickle.load(open(fpath, "rb"))
                
                # If arg_check is requested check the arguments.
                # When the check is requested, the cached result is 
                # stored on disk with a tuple of 4 elements:
                # (`result`, args, kwargs, MAGIC)
                # where `result` is the cached function result, args
                # and kwargs are the argument of the function producing
                # `result`.
                is_cached_tuple = (hasattr(cached, '__len__') and len(cached) == 4 and
                        cached[3] == MAGIC)
                if not arg_check or (is_cached_tuple and cached[1] == args and
                        cached[2] == kwargs):
                    
                    print("'{}' not executed, result loaded from disk".format(func.__name__))
                    return cached[0] if is_cached_tuple else cached


            # Cache file not present or argcheck failed. Execute the
            # function and dump the result on the file. Return then the result
            result = func(*args, **kwargs)
            to_cache = result if not arg_check else (result, args, kwargs, MAGIC)
            try:
                pickle.dump(to_cache, open(fpath, "wb"))
            except Exception as e:
                print("Exception", e.__class__, "occurred while caching",func.__name__ ,"result")
                print("Trying to not save arguments...")
                pickle.dump(result, open(fpath, "wb"))

            return result

        return wrapper

    return decorator


