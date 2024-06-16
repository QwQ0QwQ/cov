import asyncio
from playwright.async_api import async_playwright
import time
import click
import logging
import sys


async def maketest(url, browser_string, testcase, logger, verbose=True, headless=True):
    async with async_playwright() as playwright:

        logger.info(f"[+] Starting Browser: {browser_string}")
        start = time.time()
        # Browser selection
        if browser_string == 'chrome' or browser_string == 'chromium':
            browser = await playwright.chromium.launch(headless=headless)
        elif browser_string == 'firefox':
            browser = await playwright.firefox.launch(headless=headless)
        elif browser_string == 'webkit':
            browser = await playwright.webkit.launch(headless=headless)
        elif browser_string == 'brave':
            browser = await playwright.chromium.launch(headless=headless, executable_path='/usr/bin/brave-browser')
        else:
            raise Exception('Browser not supported')

        # Open a new page
        page = await browser.new_page(ignore_https_errors=True)

        # Verbose output
        if verbose:
            page.on("console", lambda msg: logger.info(f"[$] {msg.text}"))

        logger.info(f"[+] Creating {testcase['test_name']} Test for {url}")
        # Don't trust this, let's be safe (delay)
        await asyncio.sleep(1)

        with open(testcase['test_file'], 'r') as f:
            js_code = f.read()

        encapsulated_js_code = f"""
                   (url) => {{
                           {js_code}
                            return leak(url);
                       }}
               """.strip()
        # Inject the encapsulated JS code (assuming no imports)
        print(encapsulated_js_code)
        try:
            result=await page.evaluate(encapsulated_js_code, url)
            logger.info(f"[+] Test Successful")
        except TimeoutError:
            # Handle timeout specifically
            logger.error(f"[-] Test Timed Out ({testcase['test_timeout']} seconds)")
            result = 0  # Or handle the timeout differently as needed
        except Exception as e:
            # Handle other errors
            logger.error(f"[-] Error: {e}")
            result = 0  # Or handle the error differently as needed

        logger.info(f"[+] Test: Done, Closing Browser")
        logger.info(f"[+] Time: {time.time() - start}")
        print(result)
        await page.close()
        return result


@click.command()
@click.option('--url', '-u', help='URL to crawl', required=True)
@click.option('--browser', '-b', help='Browser to use', default='chrome')
@click.option('--verbose', '-v', help='Verbose output', is_flag=True, default=False)
@click.option('--headfull', '-hf', help='Disable Headless mode', is_flag=True, default=True)
def commandLine(url, browser, filepath,verbose, headfull):
    # Setup logging
    logger = logging.getLogger()
    streamHandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)

    print(asyncio.run(maketest(url, browser,filepath, logger,verbose=verbose, headless=headfull)))


if __name__ == '__main__':
    commandLine()
