from termcolor import colored


class RecordForSummaryReporter:
    def __init__(self, reporter):
        self.reporter = reporter
        self.print_statements = []
        self._reset()

    def record_message(self, print_statements=None):
        if print_statements is not None:
            for print_statement in print_statements:
                if print_statement is not None:
                    self.print_statements.append(((colored("| ", 'blue', None, ['bold']),), {"end": ""}))
                    print_params, print_kwargs = print_statement
                    result_params = []
                    for param in print_params:
                        if isinstance(param, str):
                            result_params.append(param.replace('\n', colored("\n| ", 'blue', None, ['bold'])))
                        else:
                            result_params.append(param)

                    self.print_statements.append((result_params, print_kwargs))

    def _reset(self):
        self.print_statements = []

    def reset(self):
        self._reset()
        self.record_message(self.reporter.reset())

    def report_enter_context(self, describe_block):
        self.record_message(self.reporter.report_enter_context(describe_block))

    def report_exit_context(self, describe_block):
        self.record_message(self.reporter.report_exit_context(describe_block))

    def report_failure(self, failed_behavior, it_block, filtered_exception, timing_millis):
        self.record_message(self.reporter.report_failure(failed_behavior, it_block, filtered_exception, timing_millis))

    def report_success(self, it_block, timing_millis):
        self.record_message(self.reporter.report_success(it_block, timing_millis))

    def report_pending(self, it_block):
        self.record_message(self.reporter.report_pending(it_block))

    def report_end_result(self):
        self.record_message(self.reporter.report_end_result())
        return self.print_statements
