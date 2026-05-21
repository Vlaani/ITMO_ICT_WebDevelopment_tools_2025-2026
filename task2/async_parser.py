import sys
import os
from pathlib import Path
root_dir = Path(os.getcwd()).parent / 'app'
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import time
from typing import Any
import asyncio
import json
from playwright.async_api import async_playwright

from db.db import init_db
from DBSaver import save_to_db

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

async def parse_and_save(page, url, background_tasks):
    """Открывает страницу и сразу отправляет её на фоновую обработку."""
    print(f"[OPEN] {url}\n")
    await page.goto(url, wait_until="load")

async def tab_worker(page, queue, background_tasks):
    """Воркер для конкретной вкладки. Берет URL из очереди, пока они не кончатся."""
    while True:
        try:
            url = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        
        try:
            await parse_and_save(page, url, background_tasks)
        except Exception as e:
            print(f"Ошибка при обработке {url}: {e}")
        finally:
            queue.task_done()

start : float = 0

async def main():
    init_db()

    queue = asyncio.Queue()
    for url in URLS:
        await queue.put(url)
        
    background_tasks = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = await browser.new_context()

        async def on_response(response):
            if TARGET in response.url and "productId" in response.url:
                data = await response.text()
                try:
                    print(f"[URL] {response.url}\n[DATA] {data[128:]}...\n----------------------------------------------------------------\n")
                    json_data = prepare_response(data)
                    if json_data['ret'][0].startswith("SUCCESS"):
                        task = asyncio.create_task(save_to_db(json_data))
                        background_tasks.add(task)
                    else:
                        print(f"Unseccessful, [DATA] {data}")
                except Exception as e:
                    print(f"Данные {data[data.find('{'):-1]} не удаётся распарсить, \nexception: {e}\n")

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
            page.context.on("response", on_response)
            pages.append(page)         

        workers = [
            asyncio.create_task(tab_worker(page, queue, background_tasks)) 
            for page in pages
        ]
        
        await asyncio.gather(*workers)
        print("Все URL были успешно открыты вкладками.")
        
        if background_tasks:
                print(f"Ожидаем завершения оставшихся обработок: {len(background_tasks)} шт.")
                await asyncio.gather(*background_tasks)
                
        print("Вся обработка полностью завершена!")
            
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
    end = time.time()
    print(f"Время работы: {end - start}")
