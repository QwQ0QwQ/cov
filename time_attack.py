from h2time import H2Time, H2Request
import logging
import asyncio

ua = 'h2time/0.1'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('h2time')

async def run_two_gets():
    r1 = H2Request('GET', 'http://baidu.com/', {'user-agent': ua})
    r2 = H2Request('GET', 'http://baidu.com/?2', {'user-agent': ua})
    logger.info('Starting h2time with 2 GET requests')
    async with H2Time(r1, r2, num_request_pairs=5) as h2t:
        results = await h2t.run_attack()
        print('\n'.join(map(lambda x: ','.join(map(str, x)), results)))
    logger.info('h2time with 2 GET requests finished')

loop = asyncio.get_event_loop()
loop.run_until_complete(run_two_gets())

loop.close()
