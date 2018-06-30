class BehaviorBlock:
    def __init__(self, parent, method, description):
        self.method = method
        self.parent = parent
        self.description = description

    def run(self):
        pass


class DescribeBlock(BehaviorBlock):
    def __init__(self, parent, context_description, method):
        class Context(object):
            def __init__(self):
                if parent is not None:
                    for attr in dir(parent.context):
                        if not hasattr(self, attr):
                            setattr(self, attr, getattr(parent.context, attr))

        super().__init__(parent, method, context_description)
        self.describe_blocks = []
        self.before_each_blocks = []
        self.it_blocks = []
        self.context = Context()


class ItBlock(BehaviorBlock):

    @staticmethod
    def pending():
        pass

    def __init__(self, parent, description, method):
        super().__init__(parent, method, description)

    def run(self):
        try:
            self.method()
        except Exception as e:
            print("Test failed: " + self.description)
            raise e


class BeforeEachBlock(BehaviorBlock):
    def __init__(self, parent, method):
        super().__init__(parent, method, "@before_each")

    def run(self):
        self.method()