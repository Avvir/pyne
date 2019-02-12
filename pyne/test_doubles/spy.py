class Spy:
    def __init__(self, stubbed_object=None, method=None, call_method=True):
        self.method = method
        self.stubbed_object = stubbed_object
        self.last_call = None
        self.return_value = None
        self.call_method = call_method

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
        if self.call_method:
            self.return_value = self.method(*args, **kwargs)
        return self.return_value

    def returns(self, return_value):
        self.return_value = return_value

    def restore(self):
        self.last_call = None
        self.return_value = None
        if self.stubbed_object is not None:
            if isinstance(self.stubbed_object, type):
                setattr(self.stubbed_object, self.method.__name__, self.method)
            else:
                self.stubbed_object.__setattr__(self.method.__name__, self.method)

def spy(object_to_stub, method):
    spy = Spy(object_to_stub, method, call_method=True)

    if isinstance(object_to_stub, type):
        setattr(object_to_stub, method.__name__, spy)
    else:
        object_to_stub.__setattr__(method.__name__, spy)
    return spy
