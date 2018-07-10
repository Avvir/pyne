from time import sleep

from termcolor import colored


class PyneStats:
    def __init__(self):
        self.is_failure = False
        self.test_count = 0
        self.pass_count = 0
        self.failure_count = 0
        self.pending_count = 0
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
        self.stats.failure_count += 1
        self.stats.test_count += 1
        self.stats.is_failure = True
        self.stats.total_timing_millis += timing_millis

    def report_success(self, it_block, timing_millis):
        self.stats.pass_count += 1
        self.stats.test_count += 1
        self.stats.total_timing_millis += timing_millis

    def report_pending(self, it_block):
        self.stats.pending_count += 1
        self.stats.test_count += 1

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
        elif self.stats.test_count == 0:
            raise NoTestsException()


class PyneStatSummaryReporter(StatTrackingReporter):
    def report_end_result(self):
        StatTrackingReporter.report_end_result(self)

        if self.stats.test_count == 0:
            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 Ran 0 tests 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲'
            print(stats)

        else:
            failures = "{0} failed, ".format(self.stats.failure_count) if self.stats.failure_count > 0 else ""
            pendings = ", {0} pending".format(self.stats.pending_count) if self.stats.pending_count > 0 else ""

            stats = '\n🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲 ' \
                    '{failures}{pass_count} passed{pendings} in {seconds:0.2f} seconds' \
                    ' 🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲' \
                .format(
                pendings=pendings,
                failures=failures,
                pass_count=self.stats.pass_count,
                seconds=self.stats.total_timing_millis / 1000)
            print(stats)


class PyneDotReporter(StatTrackingReporter):
    def reset(self):
        StatTrackingReporter.reset(self)

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        StatTrackingReporter.report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis)
        print("x", end="")

    def report_pending(self, it_block):
        StatTrackingReporter.report_pending(self, it_block)
        print("-", end="")

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

    def report_pending(self, it_block):
        StatTrackingReporter.report_pending(self, it_block)
        print(colored(" -", 'yellow') + "  " * self.depth + colored(it_block.description, 'yellow', None, ['dark']))


class PyneFailureSummaryReporter(StatTrackingReporter):
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

    def report_pending(self, it_block):
        for reporter in self.reporters:
            reporter.report_pending(it_block)


reporter = CompositeReporter(PyneTreeReporter(), PyneStatSummaryReporter(), PyneFailureSummaryReporter(), ExceptionReporter())
