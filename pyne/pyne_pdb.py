from . import pyne_test_runner
import pdb
import sys
pdb_enabled = "--pdb" in sys.argv
if pdb_enabled and "--pdb" in sys.argv:
    sys.argv.remove("--pdb")

def debug_block(name):
    print("Error handling '%s' block." % name)
    print("Entering pdb post-mortem")
    pdb.pm()
    print("Rerunning '%s' block with pdb." % name)
    pdb.set_trace()

def handle_before_failure(context, before_blocks):
    debug_block("before")
    pyne_test_runner.run_blocks(before_blocks, context)

def handle_it_failure(context, before_blocks, it_block):
    pyne_test_runner.run_blocks(before_blocks, context)
    debug_block("it")
    pyne_test_runner.run_blocks([it_block], context)

def handle_after_failure(context, before_blocks, it_block, after_blocks):
    pyne_test_runner.run_blocks(before_blocks, context)
    pyne_test_runner.run_blocks([it_block], context)
    debug_block("after")
    pyne_test_runner.run_blocks(after_blocks, context)
