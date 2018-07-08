class PyneResultReporter:
    def __init__(self, _print=print):
        self._print = _print
        self.failed = False
        self.has_run_behavior = False

    def reset(self):
        self.failed = False
        self.has_run_behavior = False

    def report_result(self, context, before_blocks, it_block):
        self.has_run_behavior = True
        for before_block in before_blocks:
            try:
                before_block.method(context)
            except Exception as e:
                self.failed = True
                self._print("x", end="")
                self._print(before_block.description)
                self._print(it_block.description)
                self._print(e)
                return

        try:
            it_block.method(context)
            self._print(".", end="")
        except Exception as e:
            self.failed = True
            self._print("x", end="")
            self._print(it_block.description)
            self._print(e)

    def combine_ancestor_descriptions(self, ancestors_description, inner_description):
        pass

    def report_end_result(self):
        if self.failed:
            raise Exception("Tests failed.")
        elif not self.has_run_behavior:
            raise Exception("No tests to run!")
        else:
            self._print("Success!")


reporter = PyneResultReporter()
