class TemporaryClass:
    def __enter__(self):
        class SomeTemporaryClass:
            @staticmethod
            def some_static_method(*args, **kwargs):
                pass

            @staticmethod
            def some_other_static_method(*args, **kwargs):
                pass

            def some_method(self, *args, **kwargs):
                pass

            def some_other_method(self, *args, **kwargs):
                pass

        return SomeTemporaryClass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass