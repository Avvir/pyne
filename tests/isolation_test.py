import io
import sys

from pyne.expectations import expect
from pyne.matchers import contains


def test__replacing_stdout_as_if_in_multiple_tests():
    charset = 'utf-8'
    bytes_output = io.BytesIO()
    sys.stdout = sys.stderr = io.TextIOWrapper(
        bytes_output, encoding=charset)

    print("hello world")
    sys.stdout.flush()
    output = bytes_output.getvalue().decode(charset)
    expect(output).to_be("hello world\n")

    bytes_output = io.BytesIO()
    sys.stdout = sys.stderr = io.TextIOWrapper(
        bytes_output, encoding=charset)

    print("what a world you are")
    sys.stdout.flush()
    output = bytes_output.getvalue().decode(charset)
    expect(output).to_be("what a world you are\n")


def test__the_same_test_again_basically():
    charset = 'utf-8'
    bytes_output = io.BytesIO()
    sys.stdout = sys.stderr = io.TextIOWrapper(
        bytes_output, encoding=charset)

    print("hello Bob")
    sys.stdout.flush()
    output = bytes_output.getvalue().decode(charset)
    expect(output).to_be("hello Bob\n")

    bytes_output = io.BytesIO()
    sys.stdout = sys.stderr = io.TextIOWrapper(
        bytes_output, encoding=charset)

    print("what are you up to, Bob")
    sys.stdout.flush()
    output = bytes_output.getvalue().decode(charset)
    expect(output).to_be("what are you up to, Bob\n")
