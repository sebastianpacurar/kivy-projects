import os
from functools import wraps

from kivy.clock import Clock


def explicit_wait(wait=0.5, callback=None):
    """ Display Loading Spinner for given wait in seconds \n
        Pass in the callback function for which the wait is performed, and provide the result param \n
        Result is the api response
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Clock.schedule_once(lambda dt: args[0].app.show_spinner(wait), 0)
            result = func(*args, **kwargs)
            if callback:
                Clock.schedule_once(lambda dt: callback(args[0], result), 0)

            return result

        return wrapper

    return decorator


def find_project_root(target="README.md"):
    # go up x levels through directories until root is reached
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):  # go up one level iteratively
        if target in os.listdir(current_dir):
            return current_dir  # return directory if README.md is present
        current_dir = os.path.dirname(current_dir)  # go up one level
