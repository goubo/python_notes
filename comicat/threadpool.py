import logging
import queue
from concurrent.futures import ThreadPoolExecutor
from functools import wraps


def _deco(f):
    @wraps(f)
    def __deco(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)

    return __deco


class BoundedThreadPoolExecutor(ThreadPoolExecutor, ):
    def __init__(self, max_workers=None, thread_name_prefix=''):
        ThreadPoolExecutor.__init__(self, max_workers, thread_name_prefix)
        self._work_queue = queue.Queue(max_workers * 2)

    def submit(self, fn, *args, **kwargs):
        fn_deco = _deco(fn)
        super().submit(fn_deco, *args, **kwargs)
