# SINGLE PROCESS(=CORE) - SINGLE THREAD - SYNC
import time, os, threading, asyncio

nums = [30] * 100


async def tempfunc(numbers):
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total


async def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread")
    numbers = range(1, num)
    print("before-code")
    result = await asyncio.create_task(tempfunc(numbers))
    print("after-code")
    return result


async def main():
    results = await asyncio.gather(*[cpu_bound_func(num) for num in nums])
    # print(results)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)  # 10.35
