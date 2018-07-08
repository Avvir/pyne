def befores_to_run(describe_block):
    if describe_block.parent is None:
        return describe_block.before_each_blocks
    else:
        return befores_to_run(describe_block.parent) + describe_block.before_each_blocks


def run_tests(describe_block, result_reporter, is_top_level=True):
    for it_block in describe_block.it_blocks:
        result_reporter.report_result(describe_block.context, befores_to_run(describe_block), it_block)

    for nested_describe_block in describe_block.describe_blocks:
        run_tests(nested_describe_block, result_reporter, False)

    if is_top_level:
        result_reporter.report_end_result()
