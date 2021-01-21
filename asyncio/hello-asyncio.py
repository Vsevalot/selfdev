import asyncio
from datetime import datetime
from random import randint


def log(msg):
    print(f'{datetime.now():%H:%M:%S.%f} {msg}')


async def say_after(msg, delay):
    log(f"Message {msg} is scheduled for execution")
    await asyncio.sleep(delay)  # wait and pause the script for delay seconds
    log(msg)


async def main_with_pauses():
    log("script started")
    await say_after("Hello", 2)
    await say_after("asyncio!", 2)
    log("complete")


async def main_without_pauses():
    log("script started")
    task1 = asyncio.create_task(say_after("Hello", 2))
    task2 = asyncio.create_task(say_after("asyncio!", 2))
    await task1
    await task2
    log("complete")


async def mimic_get_request():
    result = randint(0, 10)
    while result != 0:
        try:
            result = randint(0, 10)
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            log("Cancelling get request")
            raise asyncio.CancelledError
    return "some data"


async def main_with_timeout(timeout):
    log("script started")
    for i in range(10):
        task_get = asyncio.create_task(mimic_get_request())
        log(f"sent get request, timeout = {timeout}")
        await asyncio.sleep(timeout)
        if task_get.done():
            log(f"get request completed, response = {task_get.result()}")
        else:
            task_get.cancel()
            log(f"timeout - get request froze, canceling")
        print()

    log("script completed")


if __name__ == '__main__':
    asyncio.run(main_with_timeout(3))
