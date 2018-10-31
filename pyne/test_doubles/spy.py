class Spy:
    def __init__(self, instance, method):
        self.method = method
        self.instance = instance
        self.last_call = None

    def __call__(self, *args, **kwargs):
        self.last_call = (args, kwargs)


# Stubbing classes
# def stub(clazz):
#     def decorator(method):
#         setattr(clazz, method.__name__, Spy(clazz, method))
#         return method
#
#     return decorator


def stub(instance, method):
    instance.__setattr__(method.__name__, Spy(instance, method))
