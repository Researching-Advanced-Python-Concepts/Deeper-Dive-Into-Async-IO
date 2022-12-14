import aiohttp
import queue
import multiprocessing


class Pool(multiprocessing.Pool):
    async def df_queue(self, fn, *args, **kwargs) -> int:
        # queue an individual item of work and return a task
        # id(unique)
        pass
    
    async def result(self, id) -> any:
        # await the result given the task id
        pass
    
    async def map(self, fn, items):
        task_ids = [
            await self.queue(fn, (item,), {})
            for item in items
        ]
        
        return [
            await self.result(task_id)
            for task_id in task_ids
        ]
    
async def fetch_url(url):
    return await aiohttp.request("GET", url)

async def fetch_all(urls):
    async with Pool() as pool:
        results = await pool.map(fetch_url, urls)
    
    