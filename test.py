import asyncio
import io
import time
from log import log
import logging
import requests
import os

from playwright.async_api import async_playwright


# logging is a bit of magic
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_stream = io.StringIO()
logger.addHandler(logging.StreamHandler(log_stream))

async def makeGraph():
    async with async_playwright() as playwright:


        browser = await playwright.chromium.launch(args=["--max-old-space-size=10240000"])

        # 打开一个页面
        page = await browser.new_page(ignore_https_errors=True)
        # 详细输出


        # dont trust this lets be save
        await asyncio.sleep(1)
        result = await page.evaluate(open('./src/testing.js', 'r').read())
        await page.close()
        return result
# 保存结果的文件名
output_file = "output.txt"

# 打开输出文件
async def main():
    # with open(output_file, "w") as f:
    # 遍历文件夹中的所有文件
    #     for filename in os.listdir(dir_path):
    #         # 拼接文件路径
    #         url="http://127.0.0.1:8001/"+filename
    #         G=await makeGraph(url,"chrome",logger,verbose=True,headless=False,)
    #         print(G)
    url="http://baidu.com"
    result = await makeGraph()
    print(result)



asyncio.run(main())
