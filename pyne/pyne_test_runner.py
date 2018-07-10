from time import perf_counter


def befores_to_run(describe_block):
    if describe_block.parent is None:
        return describe_block.before_each_blocks
    else:
        return befores_to_run(describe_block.parent) + describe_block.before_each_blocks


def run_tests(describe_block, result_reporter, is_top_level=True, parent_is_pending=False):
    result_reporter.report_enter_context(describe_block)

    is_pending_describe = describe_block.pending or parent_is_pending
    if is_pending_describe:
        for it_block in describe_block.it_blocks:
            result_reporter.report_pending(it_block)
    else:
        for it_block in describe_block.it_blocks:
            if it_block.pending:
                result_reporter.report_pending(it_block)
            else:
                run_test(describe_block.context, befores_to_run(describe_block), it_block, result_reporter)

    for nested_describe_block in describe_block.describe_blocks:
        run_tests(nested_describe_block, result_reporter, False, is_pending_describe)

    result_reporter.report_exit_context(describe_block)

    if is_top_level:
        result_reporter.report_end_result()


def run_test(context, before_blocks, it_block, reporter):
    start_seconds = perf_counter()
    for before_block in before_blocks:
        try:
            before_block.method(context)
        except Exception as e:
            seconds = perf_counter() - start_seconds
            reporter.report_failure(before_block, it_block, e, seconds * 1000)
            return

    try:
        it_block.method(context)
        seconds = perf_counter() - start_seconds

        reporter.report_success(it_block, seconds * 1000)
    except Exception as e:
        seconds = perf_counter() - start_seconds
        reporter.report_failure(it_block, it_block, e, seconds * 1000)
