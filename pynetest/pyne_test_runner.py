from time import perf_counter

from pynetest.pyne_pdb import is_running_inside_debugger
from . import pyne_pdb


def befores_to_run(describe_block):
    if describe_block.parent is None:
        return describe_block.before_first_blocks + describe_block.before_each_blocks
    else:
        return befores_to_run(describe_block.parent) + describe_block.before_first_blocks + describe_block.before_each_blocks


def afters_to_run(describe_block):
    if describe_block.parent is None:
        return describe_block.after_each_blocks
    else:
        return afters_to_run(describe_block.parent) + describe_block.after_each_blocks


def run_tests(describe_block, result_reporter):
    if describe_block.has_focused_descendants:
        run_only_focused_tests(describe_block, result_reporter)
    else:
        run_non_pended_tests(describe_block, result_reporter)

    result_reporter.report_end_result()


def run_non_pended_tests(describe_block, result_reporter, parent_is_pending=False):
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
                run_test(describe_block.context,
                         befores_to_run(describe_block),
                         it_block,
                         afters_to_run(describe_block),
                         result_reporter)

    for nested_describe_block in describe_block.describe_blocks:
        nested_describe_block.context = describe_block.context
        run_non_pended_tests(nested_describe_block, result_reporter, is_pending_describe)

    result_reporter.report_exit_context(describe_block)


def run_only_focused_tests(describe_block, result_reporter):
    if describe_block.focused:
        run_non_pended_tests(describe_block, result_reporter)
    else:
        result_reporter.report_enter_context(describe_block)

        for it_block in describe_block.it_blocks:
            if it_block.focused:
                run_test(describe_block.context,
                         befores_to_run(describe_block),
                         it_block,
                         afters_to_run(describe_block),
                         result_reporter)

        for nested_describe_block in describe_block.describe_blocks:
            run_only_focused_tests(nested_describe_block, result_reporter)

        result_reporter.report_exit_context(describe_block)


class BlockFailureResult:
    def __init__(self, block, exception):
        self.block = block
        self.exception = exception


def run_test(context, before_blocks, it_block, after_blocks, reporter):
    start_milliseconds = perf_counter()

    failure = run_blocks(before_blocks, context)
    if failure and pyne_pdb.pdb_enabled:
        pyne_pdb.handle_before_failure(context, before_blocks)

    if failure is None:
        failure = run_blocks([it_block], context)
        if failure and pyne_pdb.pdb_enabled:
            pyne_pdb.handle_it_failure(context, before_blocks, it_block)

    if failure is None:
        failure = run_blocks(after_blocks, context)
    else:
        after_failure = run_blocks(after_blocks, context)
        if after_failure and pyne_pdb.pdb_enabled:
            pyne_pdb.handle_after_failure(context, before_blocks, it_block, after_blocks)

    seconds = (perf_counter() - start_milliseconds) * 1000
    if failure:
        reporter.report_failure(failure.block, it_block, failure.exception, seconds)
    else:
        reporter.report_success(it_block, seconds)



def run_blocks(blocks, context):
    is_debug_mode = is_running_inside_debugger()
    for block in blocks:
        if is_debug_mode:
            block.method(context)
        else:
            try:
                block.method(context)
            except Exception as e:
                # Save traceback to enable post-mortem using pdb
                import sys
                sys.last_traceback = e.__traceback__
                return BlockFailureResult(block, e)
    return None
