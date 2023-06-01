import inspect


def format_object(object):
    try:
        if hasattr(object, '_pyne_format'):
            formatted_object = object._pyne_format()
        else:
            if isinstance(object, str):
                formatted_object = "'" + object + "'"
            elif inspect.isfunction(object):
                module_name = inspect.getmodule(object).__name__

                formatted_object = module_name + "." + object.__name__
            else:
                formatted_object = str(object)
    except Exception:
        formatted_object = str(object)
    return escape_for_formatting(formatted_object)
    # return formatted_object


def format_arguments(args_list, kwargs_dict=None):
    if kwargs_dict is None:
        kwargs_dict = dict()
    formatted_args_list = ", ".join([format_object(argument) for argument in args_list])
    formatted_kwargs_list = ", ".join(
        [format_object(key) + "=" + format_object(value) for (key, value) in kwargs_dict.items()])

    result = "("
    if len(formatted_args_list) > 0:
        result += formatted_args_list
    if len(formatted_args_list) > 0 and len(formatted_kwargs_list) > 0:
        result += ", "
    if len(formatted_kwargs_list) > 0:
        result += formatted_kwargs_list
    result += ")"
    return result


def escape_for_formatting(string):
    return string.replace("{", "{{").replace("}", "}}")
