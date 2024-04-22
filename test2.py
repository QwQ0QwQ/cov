import asyncio
import io
import time
from diff import diffGraphs
from log import log
from makeGraph import makeGraph
from model import Testcase
from datetime import datetime
import logging
import tagging

def run_testcase(basedomain, inclusionmethod, difference, filetype, browser):
    start = time.time()
    print(start)
    log(f"Started with {inclusionmethod}-{difference}-{filetype}-{browser}")
    print(f"Started with {inclusionmethod}-{difference}-{filetype}-{browser}")
    try:
        # delete the test case so we can re-run it
        Testcase.objects(
            inclusionmethod=inclusionmethod,
            difference=difference,
            filetype=filetype,
            browser=browser).delete()
    except:
        pass

    result = Testcase(
        inclusionmethod=inclusionmethod,
        difference=difference,
        filetype=filetype,
        browser=browser,
    )

    result.url = f"http://{basedomain}/test/{inclusionmethod}/{difference}/{filetype}/{browser}"
    result.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result.logs = "Running...\n"
    result.save()
    print(result.url)
    # logging is a bit of magic
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_stream = io.StringIO()
    logger.addHandler(logging.StreamHandler(log_stream))

    try:
        # create first graph
        g1 = asyncio.run(makeGraph(
            result.url,
            browser,
            verbose=True,
            headless=False,
            logger=logger
        ))
        result.logs = log_stream.getvalue()
        result.save()

        # switch state
        result.switch_state()

        # create second graph
        g2 = asyncio.run(makeGraph(
            result.url,
            browser,
            verbose=True,
            headless=False,
            logger=logger
        ))
        result.logs = log_stream.getvalue()
        result.save()

        # switch state back
        result.switch_state()

        # diff graphs and save results
        diff = diffGraphs(g1, g2)
        print("diff:")
        print(diff)
        result.diff_results.clear()
        result.diff_results.update(diff)
        result.logs = log_stream.getvalue()

        result.length = len(diff['paths'])
        # update result in db
        result.duration = f'{time.time() - start:.2f}s'
        result.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        log(f"Error {e}")
        result.logs += f'An exception occurred: {repr(e)}'
        result.save()
        raise e
    result.save()

def run_tagging():
    with open('config/tagrules.yml', 'r') as f:
        tagrules = tagging.load_tagrules(f)
    print(tagrules)
    # only get testcases that have a result
    # no_cache otherwise we run into memory issues :/
    testcases = Testcase.objects(length__ne=0).no_cache().only(
        'diff_results', 'diff_tags').order_by('-time')
    print(testcases)
    n = 0
    m = testcases.count()
    for testcase in testcases:
        n += 1
        if (n % 100 == 0):
            print(f'[Tagging] Tagged {n}/{m}')
        diffpaths = [x['path'] for x in testcase.diff_results.get(
            "structural_difference", {}).get("roots_of_change", [])]
        try:
            if diffpaths:
                tags = list(tagging.tag(diffpaths, tagrules))
                testcase.diff_tags = tags
                print(tags)
                testcase.save()
        except Exception as e:
            print('[Tagging] Error:', e)

    print('[Tagging] Done tagging!')