import traceback


def wrap(config, failures, identifier, nullary_function):
    try:
        return nullary_function()
    except Exception as e:
        if config.stop_on_first_failure:
            raise
        failures.append((identifier, traceback.format_exc()))
    return None
