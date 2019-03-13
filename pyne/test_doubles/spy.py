import inspect


class Spy:
    def __init__(self, object_to_stub=None, method=None):
        if method is not None:
            self.signature = inspect.signature(method)
        else:
            self.signature = inspect.signature(self.__call__)

        self.last_call = None
        self.return_value = None
        self.will_call_real = False
        self.stubbed_object, self.original_method = self._create_stubbed_object(object_to_stub, method)

    def _create_stubbed_object(self, object_to_stub, method):
        class Spy:
            def __init__(self):
                pass

            @staticmethod
            def __call__(self, *args, **kwargs):
                return None

        if object_to_stub is None:
            object_to_stub = Spy()

        if method is None:
            method = Spy.__call__

        setattr(object_to_stub, method.__name__, self)
        return object_to_stub, method

    def _unstub_object(self):
        setattr(self.stubbed_object, self.original_method.__name__, self.original_method)


    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
        if self.will_call_real:
            self.return_value = self.original_method(*args, **kwargs)
        return self.return_value

    def _pyne_format(self):
        stubbed_object = self.stubbed_object
        if isinstance(stubbed_object, type):
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
        self._unstub_object()
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()