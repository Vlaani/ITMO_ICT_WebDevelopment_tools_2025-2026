from playwright.sync_api import sync_playwright
import json

TARGET = "https://acs.aliexpress.com/h5/mtop.aliexpress.pdp.pc.query"

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
        ]
    )

    context = browser.new_context()

    page = context.new_page()

    # Открываем сайт
    page.goto("https://www.aliexpress.com/item/1005011890900503.html")
    page.wait_for_timeout(20000)

    print("Пройди капчу вручную...")
    input("После капчи нажми ENTER")

    print("Начинаю слушать сеть...")

    def on_response(response):
        if TARGET in response.url:
            print(f"\n<<< RESPONSE >>>")
            try:
                text = response.text()

                print("BODY:")
                print(text)

            except Exception as e:
                print("Cannot decode body:", e)

    context.on("response", on_response)

    print("\nТеперь ходим по сайту.")
    print("Все запросы будут логироваться.")
    page.goto("https://www.aliexpress.com/item/1005011890900503.html", wait_until="domcontentloaded")
    page.goto("https://www.aliexpress.com/item/1005008661998529.html", wait_until="domcontentloaded")
    page.goto("https://www.aliexpress.com/item/1005009437218184.html", wait_until="domcontentloaded")
    print("CTRL+C для выхода.")

    page.wait_for_timeout(999999999)