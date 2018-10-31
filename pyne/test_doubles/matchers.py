from pyne.matchers import equal_to_comparator, Matcher


def was_called_with(*expected_args, **expected_kwargs):
    def was_called_comparator(subject, params):
        return equal_to_comparator(subject.last_call, params)

    return Matcher("was_called_with", was_called_comparator, (expected_args, expected_kwargs))