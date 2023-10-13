# Replace the original function with another function
from typing import NamedTuple, List, Dict, Tuple


def attach_spy(parent_object, method_name, **kwargs):
    return AttachedSpy(parent_object, method_name, **kwargs)

attach_stub = attach_spy

class CallArguments(NamedTuple):
    args: List
    kwargs: Dict

class AttachedSpy:
    last_call: CallArguments
    calls: List[CallArguments]

    def __init__(self, parent_object=None, method_name=None, signature=None, needs_binding=False):
        self.parent_object = parent_object
        self.method_name = method_name
        self.signature = signature
        if not hasattr(parent_object, method_name):
            raise ValueError("No method of name %s exists on parent object %s" % (method_name, parent_object))
        self.method = getattr(parent_object, method_name)
        self.other_method_to_call = None
        self.last_call = None
        self.return_value = None
        self.return_sequence = []
        self.will_call_real = False
        self.needs_binding = needs_binding
        self.calls = []

    @property
    def spy_function(self):
        return lambda *args, **kwargs: AttachedSpy.spy_call(self, *args, **kwargs)

    @staticmethod
    def get_spy(spy_function):
        try:
            return spy_function(__get_spy__=True)
        except Exception:
            return spy_function

    @staticmethod
    def spy_call(spy_self, *args, __get_spy__=False, **kwargs):
        if __get_spy__:
            return spy_self
        if spy_self.needs_binding:
            spy_self.last_call = CallArguments(args[1:], kwargs)
        else:
            spy_self.last_call = CallArguments(args, kwargs)
        spy_self.calls.append(spy_self.last_call)
        if spy_self.other_method_to_call:
            return_value = spy_self.other_method_to_call(*args, **kwargs)
        elif spy_self.will_call_real:
            return_value = spy_self.method(*args, **kwargs)
        elif spy_self.return_sequence:
            return_value = spy_self.return_sequence.pop(0)
        else:
            return_value = spy_self.return_value
        return return_value

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

    def restore(self):
        self.unstub()

    def _reset_spy(self):
        self.last_call = None
        self.calls = []
        self.return_value = None
        self.return_sequence = []

    def call_real(self):
        self.will_call_real = True
        return self

    def then_return(self, return_value):
        self.return_value = return_value
        return self

    def then_return_sequence(self, return_values: List):
        """
        Makes the spied object/function return the next return value in the sequence.
        Once it runs out of return values, the return value will default to the then_return() value if specified.

        :param return_values: The sequence of values to return. Must be iterable.
        :return: self
        """
        try:
            self.return_sequence = list(return_values)
        except:
            ValueError(F"Error casting {return_values} to a list.")
        return self

    def then_call(self, other_to_call_method):
        self.other_method_to_call = other_to_call_method
        return self

    def then_raise(self, exception: Exception):
        def _raise(args, kwargs):
            raise exception
        self.other_method_to_call = _raise
        return self

    def _pyne_format(self):
        parent_object = self.parent_object
        if isinstance(parent_object, type):
            formatted = parent_object.__name__ + "::" + self.method_name
        else:
            formatted = parent_object.__class__.__name__ + "#" + self.method_name
        return formatted


