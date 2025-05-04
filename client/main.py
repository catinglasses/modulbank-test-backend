import time
import asyncio
import logging

from service import AsyncRequestSender

SERVER_URLS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

USER_NAMES = [
    "Kansas", "Nirvana", "Disturbed", "Manowar", "Kiss",
    "alt-J", "Ice Cube", "Grits", "The Doors", "admin"
]

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    start_time = time.perf_counter()

    request_sender = AsyncRequestSender(server_urls=SERVER_URLS, users=USER_NAMES)
    results = await request_sender.run()

    total_time = time.perf_counter() - start_time
    all_times = [timing for sublist in results for timing in sublist]

    success_requests = len(all_times)
    total_expected = 50 * 100 # Default values of AsyncRequestSender & run func
    loss_percentage = (total_expected - success_requests) / total_expected * 100

    logger.info("==========  |   RESULTS   |  ==========")
    logger.info(f"Total time: {total_time:.2f} s")
    logger.info(f"Successful requests: {success_requests}/{total_expected} ({loss_percentage:.1f}% loss)")
    logger.info(f"Throughput: {success_requests / total_time:.2f} req/s")

    if success_requests:
        avg_latency = sum(t[0] for t in all_times) / success_requests * 1000
        logger.info(f"Average latency: {avg_latency:.2f} ms")
    else:
        logger.info("All requests failed.")

if __name__ == "__main__":
    asyncio.run(main())