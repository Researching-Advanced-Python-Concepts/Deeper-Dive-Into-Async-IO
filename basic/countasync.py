import asyncio

# create a native coroutine or asynchronous generator
async def count():
    print("One")
    # pass the function control back to the event loop
    # suspends the execution of the surrounding coroutine
    await asyncio.sleep(1)
    print("Two")
    return "Result"

async def main():
    result = await asyncio.gather(count(), count(), count())
    # we get a list: ['Result', 'Result', 'Result']
    print("The result is", result)

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")