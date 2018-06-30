def befores_to_run(describe_block):
    if describe_block.parent is None:
        return describe_block.before_each_blocks
    else:
        return befores_to_run(describe_block.parent) + describe_block.before_each_blocks


def run_tests(describe_block):
    passing = True
    for it_block in describe_block.it_blocks:
        for before_block in befores_to_run(describe_block):
            before_block.method(describe_block.context)
        try:
            it_block.method(describe_block.context)
        except Exception as error:
            passing = False
    for nested_describe_block in describe_block.describe_blocks:
        run_tests(nested_describe_block)
    if not passing:
        raise Exception("Tests failed.")