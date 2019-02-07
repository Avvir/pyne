class Spy:
    def __init__(self, stubbed_object=None, method=None):
        self.method = method
        self.stubbed_object = stubbed_object
        self.last_call = None
        self.return_value = None

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
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
