import sys

printed_text = []


def fake_print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):
    for object in objects:
        printed_text.append(object)


class StubPrint:
    def __enter__(self):
        self.real_print = print
        printed_text.clear()
        globals()['__builtins__']['print'] = fake_print
        return fake_print

    def __exit__(self, *params):
        globals()['__builtins__']['print'] = self.real_print
