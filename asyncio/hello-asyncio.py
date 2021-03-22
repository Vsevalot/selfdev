import asyncio
import random
import time

# ANSI colors
colors = (
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
    "\033[0m",   # End of color
)


async def random_work_time_function(idx: int, threshold: int = 9) -> int:
    print(f"{colors[idx]}Function {idx} started.")
    random_value = random.randint(0, 10)
    seconds_of_waiting = 0
    while random_value < threshold:
        print(f"{colors[idx]}Function {idx} rolled {random_value}: still working")
        await asyncio.sleep(1)
        seconds_of_waiting += 1
        random_value = random.randint(0, 10)
    print(f"{colors[idx]}Function {idx} rolled {random_value}: COMPLETED!{colors[-1]}")
    return seconds_of_waiting


async def main():
    res = await asyncio.gather(*(random_work_time_function(i) for i in range(3)))
    return res


if __name__ == '__main__':
    start = time.time()
    r1, r2, r3 = asyncio.run(main())
    elapsed = time.time() - start
    print()
    print(f"R1 = {r1}, R2 = {r2}, R3 = {r3}")
    print(f"Completed in {elapsed: 0.1f} seconds")
