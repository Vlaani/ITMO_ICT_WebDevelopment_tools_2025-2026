import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir.parent))

import time
from typing import Any
import asyncio
import json
from playwright.async_api import async_playwright

from app.db.db import init_db
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

class AliexpressParser:
    def __init__(self):
        self.browser = None
        self.context = None
        self.pages = []
        self.background_tasks = set()
        self.playwright = None
        self.is_initialized = False
        self.queue = asyncio.Queue()
        self.workers = []
        
    def prepare_response(self, text: str) -> dict[str, Any]:
        """Парсит ответ от сервера."""
        return json.loads(text[text.find('{'):-1])
    
    async def on_response(self, response):
        """Обработчик ответов от страницы."""
        if TARGET in response.url and "productId" in response.url:
            data = await response.text()
            try:
                print(f"[URL] {response.url}\n[DATA] {data[128:]}...\n----------------------------------------------------------------\n")
                json_data = self.prepare_response(data)
                if json_data['ret'][0].startswith("SUCCESS"):
                    task = asyncio.create_task(save_to_db(json_data))
                    self.background_tasks.add(task)
                    task.add_done_callback(self.background_tasks.discard)
                else:
                    print(f"Unsuccessful, [DATA] {data}")
            except Exception as e:
                print(f"Данные {data[data.find('{'):-1]} не удаётся распарсить, \nexception: {e}\n")
    
    async def initialize(self):
        """Инициализирует браузер, проходит капчу и создаёт вкладки."""
        if self.is_initialized:
            print("Парсер уже инициализирован")
            return
        
        init_db()
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            channel="chromium",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--window-size=1280,720",
            ],
            env={
                "DISPLAY": ":99",
            },
        )
        
        self.context = await self.browser.new_context()
        
        first_page = await self.context.new_page()
        
        print("Пройди капчу вручную...")
        async with first_page.expect_request(lambda req: "acs.aliexpress.com/h5/mtop.aliexpress.pdp.pc.query/1.0/_____tmd_____/validate" in req.url and req.method == "POST", timeout=0) as request_info:
            await first_page.goto(URLS[0], timeout=0)
        #await first_page.wait_for_timeout(20000)
        print("Капча пройдена")
        
        first_page.context.on("response", self.on_response)

        self.pages = [first_page]
        
        for _ in range(TABS_COUNT - 1):
            page = await self.context.new_page()
            page.context.on("response", self.on_response)
            self.pages.append(page)
        
        self.workers = [asyncio.create_task(self.tab_worker(page)) for page in self.pages]
        
        self.is_initialized = True
        print(f"Парсер инициализирован с {len(self.pages)} вкладками")
    
    async def tab_worker(self, page):
        while True:
            url = await self.queue.get()
            print(f"[OPEN] {url}")

            try:
                print(f"[OPEN] {url}")
                await page.goto(url, wait_until="load")
            except Exception as e:
                print(f"[ERROR] {url}: {e}")
            finally:
                self.queue.task_done()
    
    async def parse_url(self, url: str) -> dict:
        """
        Открывает URL в одной из вкладок.
        Возвращает словарь с результатом операции.
        """
        if not self.is_initialized:
            return {"success": False, "error": "Парсер не инициализирован"}
                
        try:
            await self.queue.put(url)
            return {"success": True, "message": "Страница добавлена"}
        except Exception as e:
            return {"success": False, "url": url, "error": str(e)}
    
    async def parse_urls_batch(self, urls: list[str]) -> list[dict]:
        """
        Открывает несколько URL параллельно во всех вкладках.
        """
        if not self.is_initialized:
            return [{"success": False, "error": "Парсер не инициализирован"}]
        
        #queue = asyncio.Queue()
        for url in urls:
            await self.queue.put(url)
        
        all_results = await asyncio.gather(*self.workers)
        
        results = []
        for worker_results in all_results:
            results.extend(worker_results)
        
        return results
    
    async def wait_for_tasks(self):
        """Ожидает завершения всех фоновых задач сохранения."""
        if self.background_tasks:
            print(f"Ожидаем завершения {len(self.background_tasks)} фоновых задач...")
            await asyncio.gather(*self.background_tasks, return_exceptions=True)
            print("Все фоновые задачи завершены")
    
    async def close(self):
        """Закрывает браузер и освобождает ресурсы."""
        if self.browser:
            await self.wait_for_tasks()
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self.is_initialized = False
        print("Парсер остановлен")


# Глобальный экземпляр парсера
parser = AliexpressParser()

async def main():
    await parser.initialize()
    await parser.parse_urls_batch(URLS)
    
if __name__ == "__main__":
    start = time.time()
    #asyncio.run(main())
    end = time.time()
    print(f"Время работы: {end - start}")