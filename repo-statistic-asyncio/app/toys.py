from typing import Callable
import time

def stopwatches(fun: Callable) -> Callable:
    def wrapped(*args, **kwargs):
        start = time.time()
        res = fun(*args, **kwargs)
        print(f"Function run in {time.time() - start}")
        return res
    return wrapped


def async_stopwatches(async_fun):
    async def wrapped(*args, **kwargs):
        start = time.time()
        res = await async_fun(*args, **kwargs)
        print(f"Function run in {time.time() - start}")
        return res
    return wrapped
