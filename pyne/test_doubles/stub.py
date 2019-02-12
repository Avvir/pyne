from pyne.test_doubles.spy import Spy


def stub(object_to_stub, method):
    spy = Spy(object_to_stub, method, call_method=False)

    if isinstance(object_to_stub, type):
        setattr(object_to_stub, method.__name__, spy)
    else:
        object_to_stub.__setattr__(method.__name__, spy)

    return spy
