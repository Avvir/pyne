# Replace the original function with another function

def attach_spy(parent_object, method_name):
    return AttachedSpy(parent_object, method_name)

attach_stub = attach_spy


class AttachedSpy:
    def __init__(self, parent_object=None, method_name=None, signature=None):
        self.parent_object = parent_object
        self.method_name = method_name
        self.signature = signature
        if not hasattr(parent_object, method_name):
            raise ValueError("No method of name %s exists on parent object %s" % (method_name, parent_object))
        self.method = getattr(parent_object, method_name)
        self.other_method_to_call = None
        self.last_call = None
        self.return_value = None
        self.will_call_real = False

    @property
    def spy_function(self):
        return self.spy_call

    @staticmethod
    def get_spy(spy_function):
        try:
            return spy_function(__get_spy__=True)
        except Exception:
            return spy_function


    def spy_call(self, *args, __get_spy__=False, **kwargs):
        if __get_spy__:
            return self
        self.last_call = (args, kwargs)
        if self.other_method_to_call:
            self.return_value = self.other_method_to_call(*args, **kwargs)
        elif self.will_call_real:
            self.return_value = self.method(*args, **kwargs)
        return self.return_value

    def __call__(self, *args, **kwargs):
        return self.spy_call(*args, **kwargs)

    def __enter__(self):
        self.stub()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unstub()

    def stub(self):
        setattr(self.parent_object, self.method_name, self.spy_function)

    def unstub(self):
        self._reset_spy()
        setattr(self.parent_object, self.method_name, self.method)

    def _reset_spy(self):
        self.last_call = None
        self.return_value = None

    def call_real(self):
        self.will_call_real = True
        return self

    def then_return(self, return_value):
        self.return_value = return_value
        return self

    def then_call(self, other_to_call_method):
        self.other_method_to_call = other_to_call_method
        return self

    def _pyne_format(self):
        parent_object = self.parent_object
        if isinstance(parent_object, type):
            formatted = parent_object.__name__ + "::" + self.method_name
        else:
            formatted = parent_object.__class__.__name__ + "#" + self.method_name
        return formatted


def last_call_of(method):
    return AttachedSpy.get_spy(method).last_call
