class PyneStats:
    def __init__(self):
        self.is_failure = False
        self.tests_reported = 0
        self.passes_reported = 0
        self.failures_reported = 0
        self.total_timing_millis = 0


class PyneStatReporter:
    def __init__(self, _print=print):
        self.stats = PyneStats()
        self.depth = 0
        self._print = _print

    def report_enter_context(self, describe_block):
        self.depth += 1

    def report_exit_context(self, describe_block):
        self.depth -= 1

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        self.stats.failures_reported += 1
        self.stats.tests_reported += 1
        self.stats.is_failure = True
        self.stats.total_timing_millis += timing_millis

    def report_success(self, it_block, timing_millis):
        self.stats.passes_reported += 1
        self.stats.tests_reported += 1
        self.stats.total_timing_millis += timing_millis

    def report_end_result(self):
        if self.stats.is_failure:
            stats = '🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {fails} failed, {passes} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(fails=self.stats.failures_reported,
                        passes=self.stats.passes_reported,
                        seconds=self.stats.total_timing_millis / 1000)
            self._print(stats)

            raise Exception("Tests failed.")
        elif self.stats.tests_reported == 0:
            stats = '🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 Ran 0 tests 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲'
            self._print(stats)

            raise Exception("No tests to run!")
        else:
            stats = '🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {count} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(count=self.stats.tests_reported,
                        seconds=self.stats.total_timing_millis/1000)
            self._print(stats)


class PyneDotReporter:
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


reporter = PyneDotReporter()
