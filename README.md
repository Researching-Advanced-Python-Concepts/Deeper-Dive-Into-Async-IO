# Deeper-Dive-Into-Async-IO

[Following](https://realpython.com/async-io-python/)

## Keywords

- **Parallelism** consists of performing multiple operations at the same time.
- **Multiprocessing** is a means to effect parallelism, and it entails spreading tasks over a computer’s central processing units (CPUs, or cores). Best for CPU bound tasks like heavy calculations
- **Concurrency** is a slightly broader term than parallelism. It suggests that multiple tasks have the ability to run in an overlapping manner.
- **Threading** is a concurrent execution model whereby multiple threads take turns executing tasks. Used for I/O bound tasks like waiting for response from a web request.
- **a coroutine** is a function that can suspend its execution before reaching return, and it can indirectly pass control to another coroutine for some time.
- **event loop** can be thought of as something like a while True loop that monitors coroutines, taking feedback on what’s idle, and looking around for things that can be executed in the meantime. It is able to wake up an idle coroutine when whatever that coroutine is waiting on becomes available.

## Working of await

- If Python encounters an `await f()` expression in the scope of `g()`, this is how await tells the event loop, “Suspend execution of g() until whatever I’m waiting on—the result of f()—is returned. In the meantime, go let something else run.”

    ```py
    async def g():
        # Pause here and come back to g() when f() is ready
        r = await f()
        return r
    ```

- to call await the object must either be
    1. another coroutine
    2. an object defining an `.__await__()` dunder method that returns an iterator


## Things to look into for further improvement

- if parse was heavy or more intensive process we might want to consider running that in its own process with `loop.run_in_executor()`
- Default `ClientSession` has an adapter with a maximum of 100 open connections. To change that, we can pass `asyncio.connector.TCPConnector` to `ClientSession`. we can also specify limits on a per-host basis.
- specify timeouts for both session as a whole and for individual requests
- To make webcrawler recursive we can use `aio-redis` to keep track of which URLs have been crawled within the tree to avoid requesting them twice, and connect links with Python's networkx library