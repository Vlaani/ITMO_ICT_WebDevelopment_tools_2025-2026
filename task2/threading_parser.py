import sys
import os
from pathlib import Path

root_dir = Path(os.getcwd()).parent / 'app'
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Any
import asyncio
import json
import threading
from concurrent.futures import ThreadPoolExecutor

from playwright.async_api import async_playwright

from db.db import init_db
from DBSaver import save_to_db
import time

TARGET = "https://acs.aliexpress.com/h5/mtop.aliexpress.pdp.pc.query"

URLS = [
    "https://www.aliexpress.com/item/1005012135361594.html",
    "https://www.aliexpress.com/item/1005012118320125.html",
    "https://www.aliexpress.com/item/1005012135361594.html",
    "https://www.aliexpress.com/item/1005012195502736.html",
    "https://www.aliexpress.com/item/1005012322290201.html",
    "https://www.aliexpress.com/item/1005012324502255.html",
]

TABS_COUNT = 2


def prepare_response(text: str) -> dict[str, Any]:
    return json.loads(text[text.find('{'):-1])


def save_in_thread(json_data):
    """
    threading-обработка
    """
    asyncio.run(save_to_db(json_data))


async def parse_and_save(json_data, executor):
    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        executor,
        save_in_thread,
        json_data
    )


async def tab_worker(page, queue, executor):

    while True:
        try:
            url = queue.get_nowait()
        except asyncio.QueueEmpty:
            break

        try:
            print(f"[OPEN] {url}")
            await page.goto(url, wait_until="load")

        except Exception as e:
            print(f"Ошибка: {e}")

        finally:
            queue.task_done()

start: float = 0

async def main():

    init_db()

    queue = asyncio.Queue()

    for url in URLS:
        await queue.put(url)

    executor = ThreadPoolExecutor(max_workers=4)

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
        )

        context = await browser.new_context()

        async def on_response(response):
            if TARGET in response.url and "productId" in response.url:
                try:
                    data = await response.text()
                    json_data = prepare_response(data)

                    if json_data['ret'][0].startswith("SUCCESS"):
                        asyncio.create_task(parse_and_save(json_data, executor))

                except Exception as e:
                    print(e)
        
        page = await context.new_page()
        page.context.on("response", on_response)
        await page.goto(URLS[0])
        await page.wait_for_timeout(15000)
        
        print("Пройди капчу вручную...")
        input("После прохождения капчи нажми ENTER")
        
        global start
        start = time.time()
        pages = [page]

        for _ in range(TABS_COUNT - 1):
            page = await context.new_page()
            page.on("response", on_response)
            pages.append(page)

        workers = [
            asyncio.create_task(tab_worker(page, queue, executor))
            for page in pages
        ]

        await asyncio.gather(*workers)

        await browser.close()

        executor.shutdown(wait=True)


if __name__ == "__main__":
    asyncio.run(main())
    end = time.time()
    print(f"Время работы: {end - start}")