class Spy:
    def __init__(self, stubbed_object=None, method=None):
        self.method = method
        self.stubbed_object = stubbed_object
        self.last_call = None
        self.return_value = None
        self.will_call_real = False

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
        if self.will_call_real:
            self.return_value = self.method(*args, **kwargs)
        return self.return_value

    def call_real(self):
        self.will_call_real = True
        return self

    def then_return(self, return_value):
        self.return_value = return_value
        return self

    def restore(self):
        self.last_call = None
        self.return_value = None
        if self.stubbed_object is not None:
            setattr(self.stubbed_object, self.method.__name__, self.method)
        return self
