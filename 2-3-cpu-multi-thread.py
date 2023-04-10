# CONCERRENCY (그러나, 파이썬의 GIL때문에, PARALLELISM은 불가능)
# SINGLE PROCESS(=CORE) - MULTI THREAD - ASYNC
import time, os, threading
from concurrent.futures import ThreadPoolExecutor

nums = [30] * 100

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread, {num}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

def main():
    executor = ThreadPoolExecutor(max_workers=30)
    results = list(executor.map(cpu_bound_func, nums))
    # print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 10.02 sec
