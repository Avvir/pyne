from termcolor import colored


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

    def reset(self):
        self.stats = PyneStats()
        self.depth = 0

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
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {fails} failed, {passes} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(fails=self.stats.failures_reported,
                        passes=self.stats.passes_reported,
                        seconds=self.stats.total_timing_millis / 1000)
            self._print(stats)

            raise Exception("Tests failed.")
        elif self.stats.tests_reported == 0:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 Ran 0 tests 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲'
            self._print(stats)

            raise Exception("No tests to run!")
        else:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {count} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(count=self.stats.tests_reported,
                        seconds=self.stats.total_timing_millis / 1000)
            self._print(stats)


class PyneDotReporter(PyneStatReporter):
    def __init__(self, _print=print):
        super().__init__(_print)

    def reset(self):
        PyneStatReporter.reset(self)

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        PyneStatReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        self._print("x", end="")

    def report_success(self, it_block, timing_millis):
        PyneStatReporter.report_success(self, it_block, timing_millis)
        self._print(".", end="")


class PyneTreeReporter(PyneStatReporter):
    def report_enter_context(self, describe_block):
        PyneStatReporter.report_enter_context(self, describe_block)
        self._print(colored("  " * self.depth + describe_block.description, None, None, ['bold']))

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        PyneStatReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        if failed_behavior != it_block:
            self._print(colored("  " + "  " * self.depth + failed_behavior.description, 'red'))

        self._print(colored(" x" + "  " * self.depth + it_block.description, 'red'))

    def report_success(self, it_block, timing_millis):
        PyneStatReporter.report_success(self, it_block, timing_millis)
        self._print(colored(" ✓", 'green') + "  " * self.depth + colored(it_block.description, 'white', None, ['dark']))


reporter = PyneTreeReporter()
