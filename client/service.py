import time
import random
import aiohttp
import asyncio
from typing import Optional
from datetime import datetime

class AsyncRequestSender:
    def __init__(self, server_urls: list[str], users: list[str], requests_per_worker: int = 100):
        self.server_urls = server_urls
        self.users = users
        self.requests_per_worker = requests_per_worker

    async def send_request(self, session: aiohttp.ClientSession, server_url: str, sender: str) -> tuple[float, Optional[dict]]:
        text = f"{sender}'s message -- {datetime.now().isoformat()}"
        payload = {
            "sender": sender,
            "text": text
        }
        url = server_url + "/create-message"
        start_time = time.perf_counter()

        try:
            async with session.post(url=url, json=payload) as response:
                response_json = await response.json()
                if response.status != 200:
                    return -1, None
                return time.perf_counter() - start_time, response_json

        except Exception:
            return -1, None

    async def worker(self, session: aiohttp.ClientSession, worker_id: int) -> list[tuple[float, Optional[dict]]]:
        times = []
        for _ in range(self.requests_per_worker):
            url = random.choice(self.server_urls)
            user = random.choice(self.users)
            elapsed, response_json = await self.send_request(session=session, server_url=url, sender=user)
            if elapsed > 0:
                times.append((elapsed, response_json))

        return times

    async def run(self, workers_num: int = 50) -> list[list[tuple[float, Optional[dict]]]]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.worker(session, worker_id) for worker_id in range(workers_num)
            ]

            return await asyncio.gather(*tasks)
