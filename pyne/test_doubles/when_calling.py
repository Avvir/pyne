from pyne.test_doubles.spy import Spy


def when_calling(method, on=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on
    spy = Spy(object_to_stub, method)
    return spy


when = when_calling
spy_on = lambda *args, **kwargs: when_calling(*args, **kwargs).call_real()
stub = when_calling
