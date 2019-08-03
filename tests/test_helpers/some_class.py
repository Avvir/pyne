def some_decorator(fun):
    def wrapped_fun(*args, **kwargs):
        return fun(*args, **kwargs)
    return wrapped_fun


def some_module_method(*args, **kwargs):
    pass

class SomeClass:
    @classmethod
    def some_class_method(cls, *args, **kwargs):
        pass

    @staticmethod
    def some_static_method(*args, **kwargs):
        pass

    @staticmethod
    def some_other_static_method(*args, **kwargs):
        pass

    def some_method(self, *args, **kwargs):
        pass

    @some_decorator
    def some_decorated_method(self, *args, **kwargs):
        pass

    def some_other_method(self, some_first_arg, some_keyword_arg="some-default-value"):
        pass

    def some_positional_args_method(self, some_first_arg):
        pass

    def some_args_method_that_returns_some_value(self, some_first_arg, some_keyword_arg="some-default-value"):
        return "some_value"
