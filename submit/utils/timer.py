import functools
import time

import logging


def setup(logname):
    logging.basicConfig(filename=str(logname) + ".log", level=logging.DEBUG)


def timeit(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        logging.info('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsed_time * 1000))
        )

    return new_func
