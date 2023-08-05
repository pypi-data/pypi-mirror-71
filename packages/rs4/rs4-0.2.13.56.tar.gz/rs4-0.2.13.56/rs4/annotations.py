import warnings
from functools import wraps

def deprecated (msg = ""):
    def decorator (f):
        @wraps(f)
        def wrapper (*args, **kwargs):
            warnings.simplefilter ('default')
            warnings.warn (
               "{} will be deprecated{}".format (f.__name__, msg and (", " + msg) or ""),
                DeprecationWarning
            )
            return f (*args, **kwargs)
        return wrapper
    return decorator

def override (f):
    @wraps (f)
    def wrapper (*args, **karg):
        return f (*args, **karg)
    return wrapper

