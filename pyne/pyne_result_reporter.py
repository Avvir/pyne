class PyneResultReporter:
    def __init__(self, _print=print):
        self._print = _print
        self.failed = False

    def report_result(self, method_to_run):
        try:
            method_to_run()
            self._print(".", end="")
        except Exception as e:
            self.failed = True
            self._print("x", end="")
            self._print(e)

    def combine_ancestor_descriptions(self, ancestors_description, inner_description):
        pass

    def report_end_result(self):
        if self.failed:
            raise Exception("Tests failed.")
        else:
            self._print("Success!")