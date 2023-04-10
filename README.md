# CP-Programming
python concurrency / parallelism programming

[바운드와 블로킹]
- IO / CPU / 네트워크 바운드 로 인해, 블로킹이 일어남

[동기와 비동기]
- 동기: A작업 시작 - A작업 끝 - B작업 시작 - B작업 끝
- 비동기: A작업 시작 - B작업 시작 - A작업 끝 - B작업 끝


[파이썬 코루틴]
- 다양한 진입점과 탈출점이 있는 루틴
- 코루틴을 이용해 비동기 프로그래밍 구현
- async / await 으로 구현

[프로세스 / 쓰레드]
- 프로세스: 프로그램이 실행을 위해 메모리에 올라간 상태
- 쓰레드: 프로세스 내에서 CPU가 수행하는 작업의 단위
	- 싱글 쓰레드: 프로세스 내에서 한개의 쓰레드만 동작
	- 멀티 쓰레드: 프로세스 내에서 여러개의 쓰레드가 동작 
		- 다수의 쓰레드는 메모리 공유와 통신이 
		- 한 쓰레드에 문제가 생기면, 전체에 영향을 미침

[동시성(concurrency) vs 병렬성(parallelism)]
- 동시성: 한번에 여러 작업을 동시에 다루는 것을 의미 - switching!
	- 싱글 코어에서 멀티 쓰레드를 동작 시키는 방식
	- 멀티 코어에서도 동작(?)
	- 네트워크 IO BOUND 유용하게 쓰임

- 병렬성: 한번에 여러 작업을 병렬적으로 처리하는 것을 의미 - AtTheSameTime!
	- 멀티 코어에서 멀티 쓰레드를 동작 시키는 방식(=멀티 프로세싱)
	- CPU BOUND 코드에서 유용하게 쓰임

라면과 케익을 만들때에,
- 동시성 작업
	- 라면 물을 끓이고 - 스위칭 - 케익 밀가루 반죽 - 스위칭 - 라면에 스프랑 면 넣고 - 스위칭 - 오븐에 케익을 넣는다.
- 병렬성 작업
	- 사람1 - 라면 만든다.
	- 사람2 - 케익 만든다.


[멀티 쓰레딩과 멀티 프로세싱]
- 멀티 쓰레딩: 프로세스 내에서 여러개의 쓰레드가 동작
- 멀티 프로세싱: 다수의 프로세서 코어가 다수의 작업을 동시에 처리하는 것
  (=병렬성 프로그래밍)

- 파이썬에서는 하나의 자원을 동시에 여러 쓰레드가 접근하는 것을 막기위해, 
  한 번에 1개의 쓰레드만 유지하는 락인 GIL을 가지고 있다.
- 이때문에 파이썬에서는 멀티 쓰레딩으로 병렬성 연산을 수행하지 못한다.
	- 파이썬 멀티 쓰레딩은 동시성을 사용하여 IO BOUND 코드에서 유용하게 사용 
	  가능하지만, CPU BOUND 코드에서는 GIL에 의해 성능저하를 가져온다.
- 그래서 사용하는것이 멀티 프로세싱
	- 프로세스를 여러개로 복제를 해서 구현
	- 프로세스끼리 통신을 해야하기 때문에, 직렬화비용등 성능저하 가 있을수 있다.

- 일반적으로 다른 언어들에서는 멀티쓰레딩을 이용해서, 
  병렬성 프로그래밍을 할 수 있다.

# NETWORK BOUND
- 결론: 네트워크 바운드 코드는 코루틴 함수(async, await) 활용
```
# SINGLE PROCESS(=CORE) - SINGLE THREAD - SYNC
# https://2.python-requests.org/en/master/user/advanced/#id1
import requests, time, os, threading

def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text

def main():
    urls = ["https://google.com", "https://apple.com"] * 50
    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]
        # print(result)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 15.2 sec
```
```
# CONCERRENCY
# SINGLE PROCESS(=CORE) - SINGLE THREAD - ASYNC
# https://docs.aiohttp.org/en/stable/
import aiohttp, time, asyncio, os, threading

async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = ["https://google.com", "https://apple.com"] * 50
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        # print(result)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)  # 2.5 sec
```
- aiohttp에서 제공하는 코루틴 FUNC가 없다면, 어떻게 동시성 프로그램을 구현할것인가?
	- 멀티스레드로 구현!
	- 기존에 동기적으로 작성된 코드를 동시성 프로그래밍 코드로 변환할때에 사용!
	- 코루틴(async, await)으로 작성된 코드를 사용하는 것이 더 좋음
		- 어차피 GIL때문에, 병렬성 프로그래밍이 불가능
		- 쓰레드를 만들고 우선순위를 부여하는 비용이 크기 때문
		- 참고로 다른 언어들에서는 멀티쓰레딩으로 병렬성 프로그래밍 가능
```
# CONCERRENCY (그러나, 파이썬의 GIL때문에, PARALLELISM은 불가능)
# SINGLE PROCESS(=CORE) - MULTI THREAD - ASYNC
# https://docs.python.org/3.7/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
import requests, time, os, threading
from concurrent.futures import ThreadPoolExecutor

def fetcher(params):
    session = params[0]
    url = params[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text

def main():
    urls = ["https://google.com", "https://apple.com"] * 50

    executor = ThreadPoolExecutor(max_workers=30)

    with requests.Session() as session:
        # result = [fetcher(session, url) for url in urls]
        # print(result)
        params = [(session, url) for url in urls]
        results = list(executor.map(fetcher, params))
        # print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 2 sec
```

# CPU BOUND
- 결론: CPU BOUND 코드는 멀티 프로세싱 사용
- 파이썬 멀티 쓰레딩은 동시성을 사용하여 NETWORK IO BOUND 
  코드에서 유용하게 사용할 수 있지만, 
  CPU BOUND 코드에서는 GIL때문에 원하는만큼 성능이 나오지 않는다.
  이때, <멀티 프로세싱을 통해 성능의 이점을 취한다.>
```
# SINGLE PROCESS(=CORE) - SINGLE THREAD - SYNC
import time, os, threading

nums = [30] * 100

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

def main():
    results = [cpu_bound_func(num) for num in nums]
    # print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 10.35
```
```
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

```
```
# CONCERRENCY, PARALLELISM
# MULTI PROCESS(=CORE) - MULTI THREAD - ASYNC
import time, os, threading
from concurrent.futures import ProcessPoolExecutor

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
    executor = ProcessPoolExecutor(max_workers=10)
    results = list(executor.map(cpu_bound_func, nums))
    # print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 2.13
```