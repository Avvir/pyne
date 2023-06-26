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
    def __init__(self, parent, context_description, method, pending=False, focused=False, has_focused_descendants=False):
        super().__init__(parent, method, context_description)
        self.after_each_blocks = []
        self.describe_blocks = []
        self.before_first_blocks = []
        self.before_each_blocks = []
        self.it_blocks = []
        self.context = Context(parent)
        self.pending = pending
        self.has_focused_descendants = has_focused_descendants
        self.focused = focused


class ItBlock(BehaviorBlock):

    def __init__(self, parent, description, method, pending=False, focused=False):
        super().__init__(parent, method, description)
        self.pending = pending
        self.focused = focused


class BeforeEachBlock(BehaviorBlock):
    def __init__(self, parent, method):
        super().__init__(parent, method, "@before_each")


class BeforeFirstBlock(BehaviorBlock):
    def __init__(self, parent, method):
        self.has_run = False
        super().__init__(parent, self.run_method_if_first, "@before_first")
        self.before_first_method = method

    def run_method_if_first(self, *args, **kwargs):
        if not self.has_run:
            self.has_run = True
            return self.before_first_method(*args, **kwargs)


class AfterEachBlock(BehaviorBlock):
    def __init__(self, parent, method):
        super().__init__(parent, method, "@after_each")
