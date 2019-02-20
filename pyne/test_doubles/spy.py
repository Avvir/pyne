import inspect


class Spy:
    def __init__(self, stubbed_object=None, method=None):
        self.original_method = method

        if method is not None:
            self.signature = inspect.signature(method)
        else:
            self.signature = inspect.signature(self.__call__)

        self.stubbed_object = stubbed_object
        self.last_call = None
        self.return_value = None
        self.will_call_real = False

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
        if self.will_call_real:
            self.return_value = self.original_method(*args, **kwargs)
        return self.return_value

    def _pyne_format(self):
        stubbed_object = self.stubbed_object
        if stubbed_object is None:
            formatted = "spy"
        elif isinstance(stubbed_object, type):
            formatted = stubbed_object.__name__ + "::" + self.original_method.__name__
        else:
            formatted = stubbed_object.__class__.__name__ + "#" + self.original_method.__name__
        return formatted

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
            setattr(self.stubbed_object, self.original_method.__name__, self.original_method)
        return self
