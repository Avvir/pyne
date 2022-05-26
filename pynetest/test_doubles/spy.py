import inspect

from pynetest.test_doubles.attached_spy import AttachedSpy, CallArguments


class Spy:
    _validate_spy = True

    @staticmethod
    def get_spy(object):
        if isinstance(object, Spy):
            return object
        return AttachedSpy.get_spy(object)

    def __init__(self, object_to_stub=None, method=None):
        method_name = None
        if isinstance(method, str):
            method_name = method
            method = object_to_stub.__getattribute__(method)

        if method is not None:
            self.signature = inspect.signature(method)
        else:
            self.signature = inspect.signature(self.__call__)
        self.last_call = None
        self.calls = []
        self.return_value = None
        self.will_call_real = False
        self.stubbed_object, self.original_method = self._create_stubbed_object(object_to_stub, method, method_name)

    def _create_stubbed_object(self, object_to_stub, method, method_name=None):
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

        if method_name is None:
            method_name = method.__name__

        if self._validate_spy and method_name != "__call__" and not hasattr(object_to_stub, method_name):
            raise ValueError(("No method of name %s exists on parent object %s.\n" +
                              "This means Spy's introspection probably failed.\n" +
                              "Consider specifying the parent object and method name instead of method reference."
                              "e.g. when('some_method', on=some_instance)")
                             % (method_name, object_to_stub))

        self.method_name = method_name

        setattr(object_to_stub, self.method_name, self)
        return object_to_stub, method


    def _unstub_object(self):
        setattr(self.stubbed_object, self.method_name, self.original_method)

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)
        self.calls.append(self.last_call)
        if self.will_call_real:
            self.return_value = self.original_method(*args, **kwargs)
        return self.return_value

    def _pyne_format(self):
        stubbed_object = self.stubbed_object
        if isinstance(stubbed_object, type):
            formatted = stubbed_object.__name__ + "::" + self.method_name
        else:
            formatted = stubbed_object.__class__.__name__ + "#" + self.method_name
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
        self.calls = []
        self._unstub_object()
        return self

    def reset(self):
        self.last_call = None
        self.calls = []

    def __enter__(self):
        """
        For compatibility with MegaStub, with-statement
        """
        self.stub()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        For compatibility with MegaStub, with-statement
        """
        self.unstub()

    def unstub(self):
        """
        For compatibility with MegaStub
        """
        self.reset()
        self._unstub_object()

    def stub(self):
        """
        For compatibility with MegaStub
        """
        setattr(self.stubbed_object, self.method_name, self)


def last_call_of(method) -> CallArguments:
    last_call = Spy.get_spy(method).last_call
    if not isinstance(last_call, CallArguments):
        last_call = CallArguments(*last_call)
    return last_call
