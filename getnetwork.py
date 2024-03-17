import asyncio
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()

    async def handle_request(request):
        with open("requests.txt", "a") as f:
            print(f">> {request.method} {request.url}", file=f)

    async def handle_response(response):
        with open(f"responses_{response.status}.txt", "a") as f:
            print(f"<< {response.status} {response.url}", file=f)

    # 订阅请求和响应事件，并调用相应的处理函数
    page.on("request", handle_request)
    page.on("response", handle_response)

    await page.goto("https://baidu.com")
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())
