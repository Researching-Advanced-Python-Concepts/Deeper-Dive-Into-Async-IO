import asyncio
import multiprocessing
import queue
import aiohttp
import time


async def fetch_url(url):
    return await aiohttp.request("GET", url)


def fetch_all(urls):
    tx, rx = queue.Queue(), queue.Queue()
    multiprocessing.Process(
        target=bootstrap,
        args=(tx, rx)
    ).start()

    for url in urls:
        task = fetch_url, (url,), {}
        # put an item into the queue without blocking
        tx.put_nowait(task)


async def run_loop(tx, rx):
    """
    Args:
        tx (queue): work queue
        rx (queue): result queue
    """
    # limit the number of coroutine to execute
    limit = 10
    # track the no. of future currently executing
    pending = set()
    while True:
        # if fewer tasks than limit get more tasks off the work queue
        while len(pending) < limit:
            task = tx.get_nowait()
            fn, args, kwargs = task
            pending.add(fn(*args, **kwargs))

        # takes a set of future and gives back done and pending
        # we can also provide timeout here
        done, pending = await asyncio.wait(pending)
        for future in done:
            # await to get the result out of the future
            rx.put_normal(await future)
            


def bootstrap(tx, rx):
    loop = asyncio.new_event_loop()
    # set that event loop as default for the current thread or process
    asyncio.set_event_loop(loop)
    # tell event loop to execute our coroutine
    loop.run_until_complete(run_loop(tx, rx))


def main():
    urls = []
    start = time.perf_counter()
    fetch_all(urls)
    duration = time.perf_counter() - start()
    print(f"It took {duration:.2f} seconds to process {len(urls)} urls")