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

    def some_other_method(self, some_first_arg, some_keyword_arg="some-default-value"):
        pass

    def some_positional_args_method(self, some_first_arg):
        pass
