from pyne.test_doubles.spy import Spy


def when_calling(method, on=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on
    spy = Spy(object_to_stub, method)

    if isinstance(object_to_stub, type):
        setattr(object_to_stub, method.__name__, spy)
    else:
        object_to_stub.__setattr__(method.__name__, spy)

    return spy


when = when_calling
spy_on = when_calling
stub = when_calling
