"""
Some util functions
"""

import functools
import time


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapse_time = end_time - start_time
        print(f'It took {elapse_time} seconds to run {func}')
        return result

    return wrapper
