import traceback


def wrap(config, failures, identifier, nullary_function, default=None):
    """executes a function (`nullary_function`) with no arguments

    to pass arguments, use partials
    stores any exceptions in `failures`
    """
    try:
        return nullary_function()
    except Exception as e:
        if config.stop_on_first_failure:
            raise
        failures.append((identifier, traceback.format_exc()))
    return default
