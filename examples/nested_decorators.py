"""Nested decorators."""
from __future__ import print_function

class LevelCounter(object):
    """Object for 'with' to keep track of the level."""
    def __init__(self):
        self.level = 0
        self.root_stack = []

    def reset(self):
        self.level = 0
        self.root_stack = []
        
    def __enter__(self):
        self.level += 1
    
    def __exit__(self, *args):
        self.level -= 1
        level_counter.root_stack.pop()

    def __call__(self, name, string): 
        """Add a new node to the root stack."""
        node = Node(name, string)
        node.parent = level_counter.root_stack[-1]
        node.parent.children.append(node)
        level_counter.root_stack.append(node)
        return self

level_counter = LevelCounter()


class Node(object):
    """Simple class to keep track of Node info."""
    def __init__(self, name, string):
        self.name = name
        self.string = string
        self.parent = None
        self.children = []
        self.leaf_function = None

    def expand(self, level=0):
        """Recursively print string and run tests."""
        padding = "--"*level
        print("%sNode (%s): '%s'" % (padding, self.name, self.string))
        for child in self.children:
            child.expand(level+1)
        if self.leaf_function:
            print("%s%s" % (padding, self.leaf_function()))


def noop_fun():
    """This function never actually gets called."""
    raise NotImplementedError


def create_named_string_decorator(name, is_leaf=False, is_root=False):
    """Take in a name, return a string decorator with that name."""
    def string_decorator(string):
        """Take in a string, and bake it into a decorator."""
        def decorator_fun(fun):
            """Take a function, which is either a subtree or a leaf (test function)"""
            # This isn't a leaf (test) function, so execute it to expand the tree
            if is_root:
                level_counter.reset()
                level_counter.root_stack = [Node(name, string)]
            # Keep track of our level / root
            with level_counter(name, string):
                padding = "--"*level_counter.level
                # print("%sEntering level" % padding, level_counter.level)
                if is_leaf:
                    print("%sNew test function: '%s'" % (padding, string))
                    node = level_counter.root_stack[-1]
                    node.leaf_function = fun
                else:
                    print("%sNew node (%s): '%s'" %  (padding, name, string))
                    fun()
                # print("%sLeaving level" % padding, level_counter.level)
            if is_root:
                return level_counter.root_stack[0]
            return noop_fun
        decorator_fun.decorator_string = string
        return decorator_fun
    string_decorator.name = name
    string_decorator.is_leaf = is_leaf
    return string_decorator

pyne_tree = create_named_string_decorator("pyne_tree", is_root=True)
describe = create_named_string_decorator("describe")
when = create_named_string_decorator("when")
do_test = create_named_string_decorator("do_test", is_leaf=True)

### Everything above here would exist in a module """

# Define our tests in a 'pyne_tree'
print("\n\nCreating the pyne tree.\n\n")
@pyne_tree("A: this is the top most decorator")
def my_tree():
    @describe("B: this is another bit of info")
    def _(): 
        @when("C: A sub decorator")
        def _(): 
            @do_test("1: Our first test")
            def _(): 
                print("Test 1 executed!")
                return "pass"

            @do_test("2: Our Second test")
            def _(): 
                print("Test 2 executed!")
                return "pass"

        @do_test("3: Our Third test")
        def _(): 
            print("Test 3 executed!")
            return "pass"

    @do_test("4: Our fourth test")
    def _():
        print("Test 4 executed!")
        return "pass"

# my_tree is actually of type "Node", and is the root to the tree. 
# We can define tree operators, such as node.expand, to call all the tests 
# or print out information of the sub trees.  
print("\n\nExpanding the pyne tree.\n\n")
my_tree.expand()
