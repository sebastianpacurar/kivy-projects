import os
from functools import wraps
from threading import Thread

from kivy.clock import Clock


def wait_implicitly(callback):
    """
    Run the decorated function in a thread and execute the callback once it is finished \n
    Show global spinner during execution without blocking the main thread
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = {'data': None}  # store result from the thread

            def run_function():
                try:
                    # run the decorated function and store its result
                    res['data'] = func(*args, **kwargs)

                    # schedule the callback to execute in the main thread
                    Clock.schedule_once(lambda dt: callback(args[0], res['data']))

                finally:
                    # ensure the spinner is hidden after the function execution
                    Clock.schedule_once(lambda dt: args[0].app.hide_spinner())

            # show the spinner immediately
            Clock.schedule_once(lambda dt: args[0].app.show_spinner())

            # start the function in a thread
            Thread(target=run_function).start()

            # return nothing since it's non-blocking

        return wrapper

    return decorator



def find_project_root(target="README.md"):
    # go up x levels through directories until root is reached
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):  # go up one level iteratively
        if target in os.listdir(current_dir):
            return current_dir  # return directory if README.md is present
        current_dir = os.path.dirname(current_dir)  # go up one level
