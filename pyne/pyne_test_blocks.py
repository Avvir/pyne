class BehaviorBlock:
    def __init__(self, parent, method, description):
        self.method = method
        self.parent = parent
        self.description = description


class Context(object):
    def __init__(self, parent):
        if parent is not None:
            for attr in dir(parent.context):
                if not hasattr(self, attr):
                    setattr(self, attr, getattr(parent.context, attr))


class DescribeBlock(BehaviorBlock):
    def __init__(self, parent, context_description, method, pending=False):
        super().__init__(parent, method, context_description)
        self.describe_blocks = []
        self.before_each_blocks = []
        self.it_blocks = []
        self.context = Context(parent)
        self.pending = pending


class ItBlock(BehaviorBlock):

    def __init__(self, parent, description, method, pending=False):
        super().__init__(parent, method, description)
        self.pending = pending


class BeforeEachBlock(BehaviorBlock):
    def __init__(self, parent, method):
        super().__init__(parent, method, "@before_each")
