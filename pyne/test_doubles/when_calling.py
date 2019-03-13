from pyne.test_doubles.spy import Spy


def when_calling(method, on=None):
    if on is None and hasattr(method, '__self__'):
        object_to_stub = method.__self__
    else:
        object_to_stub = on
    spy = Spy(object_to_stub, method)
    return spy

def spy_on(method, on=None):
    return when_calling(method, on=on).call_real()

when = when_calling
stub = when_calling
