# SINGLE PROCESS(=CORE) - SINGLE THREAD
# https://2.python-requests.org/en/master/user/advanced/#id1
# pip install requests

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
