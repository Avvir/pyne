
class PrintingReporter:
    def __init__(self, reporter):
        self.reporter = reporter

    @staticmethod
    def print_result(print_statements=()):
        if print_statements is not None:
            for print_statement in print_statements:
                if print_statement is not None:
                    print_params, print_kwargs = print_statement
                    print(*print_params, **print_kwargs)

    def reset(self):
        self.print_result(self.reporter.reset())

    def report_enter_context(self, describe_block):
        self.print_result(self.reporter.report_enter_context(describe_block))

    def report_exit_context(self, describe_block):
        self.print_result(self.reporter.report_exit_context(describe_block))

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        self.print_result(self.reporter.report_failure(failed_behavior, it_block, filtered_exception, timing_millis))

    def report_success(self, it_block, timing_millis):
        self.print_result(self.reporter.report_success(it_block, timing_millis))

    def report_pending(self, it_block):
        self.print_result(self.reporter.report_pending(it_block))

    def report_end_result(self):
        self.print_result(self.reporter.report_end_result())

