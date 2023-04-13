# SINGLE PROCESS(=CORE) - SINGLE THREAD
# https://docs.aiohttp.org/en/stable/
# pip install aiohttp~=3.7.3

import aiohttp, time, asyncio, os, threading

async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    print("before-code")
    async with session.get(url) as response:
        print("after-code")
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
