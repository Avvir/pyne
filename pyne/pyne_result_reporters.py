from time import sleep

from termcolor import colored


class PyneStats:
    def __init__(self):
        self.is_failure = False
        self.tests_reported = 0
        self.passes_reported = 0
        self.failures_reported = 0
        self.total_timing_millis = 0


class StatTrackingReporter:
    def __init__(self):
        self.stats = PyneStats()
        self.depth = 0

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
        pass


class NoTestsException(Exception):
    def __init__(self):
        Exception.__init__(self, "No tests to run!")


class TestFailureException(Exception):
    def __init__(self):
        Exception.__init__(self, "Tests failed.")


class ExceptionReporter(StatTrackingReporter):
    def report_end_result(self):
        sleep(0.01)
        if self.stats.is_failure:
            raise TestFailureException()
        elif self.stats.tests_reported == 0:
            raise NoTestsException()


class PyneStatReporter(StatTrackingReporter):
    def report_end_result(self):
        StatTrackingReporter.report_end_result(self)

        if self.stats.is_failure:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {fails} failed, {passes} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(fails=self.stats.failures_reported,
                        passes=self.stats.passes_reported,
                        seconds=self.stats.total_timing_millis / 1000)
            print(stats)

        elif self.stats.tests_reported == 0:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 Ran 0 tests 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲'
            print(stats)

        else:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 {count} passed in {seconds:0.2f} seconds 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(count=self.stats.tests_reported,
                        seconds=self.stats.total_timing_millis / 1000)
            print(stats)


class PyneDotReporter(StatTrackingReporter):
    def reset(self):
        StatTrackingReporter.reset(self)

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        StatTrackingReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        print("x", end="")

    def report_success(self, it_block, timing_millis):
        StatTrackingReporter.report_success(self, it_block, timing_millis)
        print(".", end="")


class PyneTreeReporter(StatTrackingReporter):
    def report_enter_context(self, describe_block):
        StatTrackingReporter.report_enter_context(self, describe_block)
        print(colored("  " * self.depth + describe_block.description, None, None, ['bold']))

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        StatTrackingReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        if failed_behavior != it_block:
            print(colored("  " + "  " * self.depth + failed_behavior.description, 'red'))

        print(colored(" x" + "  " * self.depth + it_block.description, 'red'))

    def report_success(self, it_block, timing_millis):
        StatTrackingReporter.report_success(self, it_block, timing_millis)
        print(colored(" ✓", 'green') + "  " * self.depth + colored(it_block.description, 'white', None, ['dark']))


class PyneSummaryReporter(StatTrackingReporter):
    def __init__(self):
        super().__init__()
        self.failure_messages = []

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        StatTrackingReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        full_description = it_block.description
        self.failure_messages.append(
            colored("🌲 Failure: \"{full_description}\" in <{behavior_description}> ", 'red', None, ['bold']).format(
                full_description=full_description,
                behavior_description=failed_behavior.description))
        self.failure_messages.append(filtered_exception)

    def report_end_result(self):
        StatTrackingReporter.report_end_result(self)

        print("\n\n")
        for message in self.failure_messages:
            print(message)


class CompositeReporter:
    def __init__(self, *reporters):
        self.reporters = reporters

    def reset(self):
        for reporter in self.reporters:
            reporter.reset()

    def report_enter_context(self, describe_block):
        for reporter in self.reporters:
            reporter.report_enter_context(describe_block)

    def report_exit_context(self, describe_block):
        for reporter in self.reporters:
            reporter.report_exit_context(describe_block)

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        for reporter in self.reporters:
            reporter.report_failure(failed_behavior, it_block, filtered_exception, timing_millis)

    def report_success(self, it_block, timing_millis):
        for reporter in self.reporters:
            reporter.report_success(it_block, timing_millis)

    def report_end_result(self):
        for reporter in self.reporters:
            reporter.report_end_result()


reporter = CompositeReporter(PyneTreeReporter(), PyneStatReporter(), PyneSummaryReporter(), ExceptionReporter())
