import urllib

from flask import Flask, request, render_template, make_response, jsonify, send_from_directory, redirect, url_for
from model import elementgroup
from model import browsers
from model import differences
from model import inclusionmethods
from model import filetypes
from model import Testcase
from model import site_detection_results
from model import testtemplate
from bson import ObjectId
import sys
import os
import json
from functools import wraps
from mongoengine import connect, Document, StringField, ListField, disconnect, DictField
from log import log
import pymongo
import tasks
import test2
PORT = int(os.getenv('PORT', '9876'))
BIND_ADDR = os.getenv('BIND_ADDR', '0.0.0.0')
app = Flask(__name__)
# from werkzeug.middleware.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='.')
app.config['JSON_AS_ASCII'] = False
app.debug = False
connect(db='XS-Leaks')
# app.config['MONGODB_SETTINGS'] = {'db':'XS-Leaks', 'alias':'default'}
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['XS-Leaks']



# some endpoints are not available in demo mode
def demo_mode_check(func):
    @wraps(func)
    def check(*args, **kwargs):
        if os.getenv('DEMO_MODE', '0') != '0':
            return 'Error: This public instance of Autoleak is in Demo Mode.', 400
        return func(*args, **kwargs)

    return check


@app.route('/', methods=['GET'])
def index():
    difference = []
    inclusionmethod = []
    filetype = []
    browser = []
    try:
        # Fetch configuration document from the collection
        differences_datalist = differences.objects().all()
        inclusionmethods_datalist = inclusionmethods.objects().all()
        filetypes_datalist = filetypes.objects().all()
        browsers_datalist = browsers.objects().all()
        for brow in browsers_datalist:
            browser.append(brow.name)
        for include in inclusionmethods_datalist:
            inclusionmethod.append(include.name)
        for file in filetypes_datalist:
            filetype.append(file.name)
        for diff in differences_datalist:
            difference.append(diff.name)
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
        # Handle the error appropriately, potentially using defaults
    testcase_results=Testcase.objects.all()
    return render_template('app/index.html',
                           browsers=browser,
                           differences=difference,
                           inclusionmethods=inclusionmethod,
                           filetypes=filetype,
                           testcase_results=testcase_results
                           )


@app.route('/testfun')
def testfun():
    return render_template('/app/testfun.html')




@app.route('/runner', methods=['POST'])
@demo_mode_check
def runner():
    tasksamount = 0
    basedomain = "127.0.0.1:9876"
    if 'inclusionmethods' not in request.form:
        return 'inclusionmethod not found'
    if 'differences' not in request.form:
        return 'difference not found'
    if 'filetypes' not in request.form:
        return 'filetype not found'
    if 'browsers' not in request.form:
        return 'browser not found'
    print(request.form)
    try:
        for i in request.form.getlist('inclusionmethods'):
            for d in request.form.getlist('differences'):
                for f in request.form.getlist('filetypes'):
                    for b in request.form.getlist('browsers'):
                        if(not d.isalnum() or not i.isalnum() or not f.isalnum() or not b.isalnum()):
                            log('[app]', '[-] Bad Chars')
                            return 'bad chars'
                        tasksamount+=1
                        test2.run_testcase(basedomain, i, d, f, b)

    except Exception as e:
        log('[error]', f"Failed run the testcase: {e}")
    return f'{tasksamount} testcases added!'



@app.route('/site_detection', methods=['GET'])
def site_detection():
    return render_template('app/site_detection.html',
                           )

@app.route('/blank', methods=['GET'])
def blank():
    return render_template('app/blank.html',)

@app.route('/testing', methods=['GET'])
def testing():
    return render_template('app/testing.html')

@app.route('/tagconfig')
def display_tagconfig():
    # Specify the file path
    file_path = './config/tagrules.yml'

    # Read the file contents
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        # Handle file not found error
        return 'File not found!'

    # Render the template with the file content
    return render_template('app/display.html', file_content=file_content)


@app.route('/testtemplate/<_id>', methods=['GET','POST'])
def display_test_template(_id):
    # Decode the encoded filename
    result = testtemplate.objects.get(pk=_id)
    print(result.to_json())
    # Construct the file path
    file_path = '.'+result.to_json().get('test_file')

    # Check if the file exists
    if not os.path.exists(file_path):
        return 'File not found!'
    # Read the file contents
    with open(file_path, 'r') as f:
        file_content = f.read()

    # Render the template with the file content
    return render_template('app/modify_testtemplate.html', file_content=file_content,dataid=_id)


@app.route('/modify_testtemplate/', methods=['GET','POST'])
def modify_testtemplate():
    # Get the modified file content from the request form
    modified_content = request.get_json()
    print("modify")
    print(modified_content)
    # Specify the file path
    result = testtemplate.objects.get(pk=modified_content['id'])
    print(result.to_json())
    # Construct the file path
    file_path = '.' + result.to_json().get('test_file')
    # Write the modified content to the file
    try:
        with open(file_path, 'w') as f:
            f.write(modified_content['content'])

        response_data = {'message': 'File modified successfully!'}
        return json.dumps(response_data)
    except Exception as e:
        # Handle any errors during writing
        response_data = {'message': 'Error modifying file!'}
        return json.dumps(response_data)



@app.route('/modify_tagconfig', methods=['GET','POST'])
def modify_tagconfig():
    # Get the modified file content from the request form
    modified_content = request.get_json()
    print("modify")
    print(modified_content['content'])
    # Specify the file path
    file_path = './config/tagrules.yml'
    # Write the modified content to the file
    try:
        with open(file_path, 'w') as f:
            f.write(modified_content['content'])

        response_data = {'message': 'File modified successfully!'}
        return json.dumps(response_data)
    except Exception as e:
        # Handle any errors during writing
        response_data = {'message': 'Error modifying file!'}
        return json.dumps(response_data)


@app.route('/test/<inclusionmethod>/<difference>/<filetype>/<browser>')
def test(inclusionmethod, difference, filetype, browser):
    try:
        inclusionmethods_datalist = inclusionmethods.objects().all()
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
        # Handle the error appropriately, potentially using defaults
    # inclusionmethods = config.get('inclusionmethods', [])
    # crossorigindomain = os.environ.get('CROSSORIGINDOMAIN')

    i = next((i for i in inclusionmethods_datalist if i['name'] == inclusionmethod), None)

    if not i:
        return 'Inclusionmethod not found', 404

    if request.args.get('show', None):
        with open(f'./templates/inclusionmethods/{i["template"]}', 'rb') as f:
            return f.read(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    url = f"http://127.0.0.1:9876/differences/{inclusionmethod}/{difference}/{filetype}/{browser}"
    return render_template(f'inclusionmethods/{i["template"]}', url=url)


# include custom url for real world tests
@app.route('/include/<inclusionmethod>/')
def include(inclusionmethod):
    try:
        # Fetch configuration document from the collection
        differences_datalist = differences.objects().all()
        inclusionmethods_datalist = inclusionmethods.objects().all()
        filetypes_datalist = filetypes.objects().all()
        browsers_datalist = browsers.objects().all()
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
        # Handle the error appropriately, potentially using defaults
    i = next((i for i in inclusionmethods_datalist if i['name'] == inclusionmethod), None)
    if i and request.args.get('url') and request.args.get('url').startswith('http'):
        return render_template(f'inclusionmethods/{i["template"]}', url=request.args.get('url'))
    return 'Inclusionmethods or URL GET parameter not found, must start with http'


@app.route('/differences/<inclusionmethod>/<difference>/<filetype>/<browser>')
def rundifferences(inclusionmethod, difference, filetype, browser):
    try:
        # Fetch configuration document from the collection
        differences_datalist = differences.objects().all()
        filetypes_datalist = filetypes.objects().all()
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
        # Handle the error appropriately, potentially using defaults
    # check if difference and filetype are valid
    f = next((i for i in filetypes_datalist if i['name'] == filetype), None)
    if not f:
        log('[app]', f"[-] filetype not found")
        return 'filetype not found'

    d = next((i for i in differences_datalist if i['name'] == difference), None)
    if not d:
        log('[app]', f"[-] difference not found")
        return 'difference not found'

    # get difference and state from db
    try:
        result = Testcase.objects.filter(
            inclusionmethod=inclusionmethod,
            difference=difference,
            filetype=filetype,
            browser=browser
        ).only('includee_state').first()
        state = result.includee_state
        # log('[app]', f"[+] testcase {result} has state {state}")
    except:
        log('[app]', 'difference for unknown test cases requested')
        return 'difference not in database'

    # show the current diffeence as json
    if request.args.get('show', None):
        return jsonify(d['response0'], d['response1'])

    # here we get response0 or response1 depending on state
    response_dict = d['response1'] if state else d['response0']

    # get current settings with state
    if request.args.get('json', None):
        response_dict['state'] = 1 if state else 0
        return jsonify(response_dict)

    # file_type can also be set from difference
    if response_dict.get('filetype', None):
        f = response_dict.get('filetype')

    # cant use send_file because it adds etags :/
    with open(f"./filetemplates/{f['filetemplate']}", 'rb') as file:
        resp = make_response(file.read())

    resp.headers['Content-Type'] = f['contenttype']

    # set statuscode
    resp.status_code = response_dict['status']
    # set headers
    for h in response_dict['headers']:
        resp.headers[h['name']] = h['value']

    return resp


@app.route('/run/<inclusionmethod>/<difference>/<filetype>/<browser>')
@demo_mode_check
def run(inclusionmethod, difference, filetype, browser):
    basedomain = "127.0.0.1:9876"
    tasks.run_testcase.apply_async(args=[basedomain, inclusionmethod, difference, filetype, browser])
    return 'Task added!'


@app.route('/tags/start', methods=['POST'])
@demo_mode_check
def tag_start():
    # start the celery task for tagging
    test2.run_tagging()
    return "Started task of tagging all untagged results!"


@app.route('/results/<_id>')
def resultsforid(_id):
    # print(_id)
    result=site_detection_results.objects.get(pk=_id)
    print(result.to_json())
    return render_template('app/results.html',result=result.to_json())


@app.route('/results/<inclusionmethod>/<difference>/<filetype>/<browser>')
def results(inclusionmethod, difference, filetype, browser):
    result = Testcase.objects(
        inclusionmethod=inclusionmethod,
        difference=difference,
        filetype=filetype,
        browser=browser
    ).first()

    if not result:
        return jsonify('result entry not found')
    if not result.diff_results:
        return jsonify('result entry has no diff_results')
    print(jsonify(result.diff_results))
    return jsonify(result.diff_results)


@app.route('/api/elementgroup', methods=['POST'])
def api_elementgroup():
    # get post json data
    FILTERCONFIG = request.get_json(force=True)
    print("FILTERCONFIG")
    print(FILTERCONFIG)
    if not FILTERCONFIG:
        return 'filterconfig as json not found'
    # # default config
    # FILTERCONFIG = {
    #     browsers: [],
    #     onlyfindings: false,
    #     limit: 50,
    #     url: [],
    #     state: []
    # }
    dbargs = {}
    if FILTERCONFIG.get('onlyfindings'):
        dbargs['length__ne'] = 0
    if FILTERCONFIG.get('state') != []:
        dbargs['state__in'] = FILTERCONFIG.get('state')
    if FILTERCONFIG.get('url') != []:
        dbargs['url__in'] = FILTERCONFIG.get('url')
    if FILTERCONFIG.get('browser') != []:
        dbargs['browser__in'] = FILTERCONFIG.get('browser')
    # results = elementgroup.objects(**dbargs).only('url', 'inclusionmethods','state', 'domain', 'file','response','browser')
    results = elementgroup.objects(**dbargs).all()
    print(results)
    total = results.count()

    # sort
    order = request.args.get('order', default='')
    orderdir = request.args.get('dir', default='')

    if order and orderdir:
        if orderdir == '-':
            results = results.order_by('-' + order)
        else:
            results = results.order_by(order)

    # pagination
    offset = request.args.get('offset', type=int, default=-1)
    limit = request.args.get('limit', type=int, default=-1)
    if offset != -1 and limit != -1:
        results = results[offset:offset + limit]
    r = json.loads(results.to_json())
    # TODO i want a dict for the json response
    # this is not the slow part
    # response
    return {
        'results': r,
        'total': total,
    }



@app.route('/api/testfun', methods=['POST'])
def api_testfun():
    FILTERCONFIG = request.get_json(force=True)
    print("FILTERCONFIG")
    print(FILTERCONFIG)
    if not FILTERCONFIG:
        return 'filterconfig as json not found'
    # # default config
    # FILTERCONFIG = {
    #     browsers: [],
    #     onlyfindings: false,
    #     limit: 50,
    #     url: [],
    #     state: []
    # }
    results = testtemplate.objects.all()
    print(results)
    total = results.count()

    # sort
    order = request.args.get('order', default='')
    orderdir = request.args.get('dir', default='')

    if order and orderdir:
        if orderdir == '-':
            results = results.order_by('-' + order)
        else:
            results = results.order_by(order)

    # pagination
    offset = request.args.get('offset', type=int, default=-1)
    limit = request.args.get('limit', type=int, default=-1)
    if offset != -1 and limit != -1:
        results = results[offset:offset + limit]
    r = json.loads(results.to_json())
    for item in r:
        if "_id" in item:
            item["_id"] = str(ObjectId(item["_id"]["$oid"]))
    # TODO i want a dict for the json response
    # this is not the slow part
    # response
    return {
        'results': r,
        'total': total,
    }

@app.route('/api/results', methods=['POST'])
def api_results():
    # get post json data
    FILTERCONFIG = request.get_json(force=True)
    print("FILTERCONFIG")
    print(FILTERCONFIG)
    if not FILTERCONFIG:
        return 'filterconfig as json not found'

    dbargs = {}
    if FILTERCONFIG.get('onlyfindings'):
        dbargs['length__ne'] = 0
    if FILTERCONFIG.get('inclusionmethods') != []:
        dbargs['inclusionmethod__in'] = FILTERCONFIG.get('inclusionmethods')
    if FILTERCONFIG.get('differences') != []:
        dbargs['difference__in'] = FILTERCONFIG.get('differences')
    if FILTERCONFIG.get('filetypes') != []:
        dbargs['filetype__in'] = FILTERCONFIG.get('filetypes')
    if FILTERCONFIG.get('browsers') != []:
        dbargs['browser__in'] = FILTERCONFIG.get('browsers')
    print("dbargs")
    print(dbargs)
    results = Testcase.objects(**dbargs).only('inclusionmethod', 'difference', 'filetype', 'browser', 'length',
                                              'diff_tags')
    print(type(results))
    print(results)
    total = results.count()

    # sort
    order = request.args.get('order', default='')
    orderdir = request.args.get('dir', default='')

    if order and orderdir:
        if orderdir == '-':
            results = results.order_by('-' + order)
        else:
            results = results.order_by(order)

    # pagination
    offset = request.args.get('offset', type=int, default=-1)
    limit = request.args.get('limit', type=int, default=-1)
    if offset != -1 and limit != -1:
        results = results[offset:offset + limit]

    # TODO i want a dict for the json response
    # this is not the slow part
    r = json.loads(results.to_json())
    print("r:")
    print(r)
    print("total")
    print(total)
    # response
    return {
        'results': r,
        'total': total,
    }


@app.route('/api/sitedetectionresults', methods=['POST'])
def api_sitedetectionresults():
    FILTERCONFIG = request.get_json(force=True)
    print("FILTERCONFIG")
    print(FILTERCONFIG)
    if not FILTERCONFIG:
        return 'filterconfig as json not found'
    dbargs = {}
    if FILTERCONFIG.get('onlyfindings'):
        dbargs['length__ne'] = 0
    if FILTERCONFIG.get('url') != []:
        dbargs['url__in'] = FILTERCONFIG.get('url')
    print("dbargs")
    print(dbargs)
    results = site_detection_results.objects().all()
    total = results.count()
    # sort
    order = request.args.get('order', default='')
    orderdir = request.args.get('dir', default='')

    if order and orderdir:
        if orderdir == '-':
            results = results.order_by('-' + order)
        else:
            results = results.order_by(order)

    # pagination
    offset = request.args.get('offset', type=int, default=-1)
    limit = request.args.get('limit', type=int, default=-1)
    if offset != -1 and limit != -1:
        results = results[offset:offset + limit]

    # TODO i want a dict for the json response
    # this is not the slow part
    r = json.loads(results.to_json())
    print("r:")
    print(r)
    for item in r:
        if "_id" in item:
            item["_id"] = str(ObjectId(item["_id"]["$oid"]))
    print(r)
    print("total")
    print(total)
    # response
    return {
        'results': r,
        'total': total,
    }


@app.route('/api/saveresults', methods=['POST'])
def api_saveresults():
    data = request.get_json()
    print(data)
    site_detection_results(url=data.get('url'),results=data.get('results')).save()
    return f"result: {data.get('url')} add success!!"


@app.route('/admin', methods=['GET', 'POST'])
@demo_mode_check
def admin():
    difference = []
    inclusionmethod = []
    filetype = []
    browser=[]
    try:
        # Fetch configuration document from the collection
        differences_datalist=differences.objects().all()
        inclusionmethods_datalist=inclusionmethods.objects().all()
        filetypes_datalist=filetypes.objects().all()
        browsers_datalist=browsers.objects().all()
        for brow in browsers_datalist:
            browser.append(brow.name)
        for include in inclusionmethods_datalist:
            inclusionmethod.append(include.name)
        for file in filetypes_datalist:
            filetype.append(file.name)
        for diff in differences_datalist:
            difference.append(diff.name)
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
        # Handle the error appropriately, potentially using defaults

    # POST request to filter results
    if request.method == 'POST':
        if 'inclusionmethods' not in request.form:
            return 'inclusionmethod not found'
        if 'differences' not in request.form:
            return 'difference not found'
        if 'filetypes' not in request.form:
            return 'filetype not found'
        if 'browsers' not in request.form:
            return 'browser not found'

        results = Testcase.objects(
            inclusionmethod__in=request.form.getlist('inclusionmethods'),
            difference__in=request.form.getlist('differences'),
            filetype__in=request.form.getlist('filetypes'),
            browser__in=request.form.getlist('browsers')
        ).exclude('diff_results', 'logs', 'testsuite', 'url').all()

    if request.method == 'GET':
        # how many to show
        if request.args.get('n'):
            n = int(request.args.get('n'))
        else:
            n = 100

        if request.args.get('findings'):
            # return only findings where Testcase.length != 0
            results = Testcase.objects(length__ne=0).exclude('diff_results', 'logs', 'testsuite', 'url').all()
        else:
            # return only latest testcases
            results = Testcase.objects.exclude('diff_results', 'logs', 'testsuite', 'url').order_by('-time').limit(n)
    return render_template('app/admin.html',
                           browsers=browser,
                           differences=difference,
                           inclusionmethods=inclusionmethod,
                           filetypes=filetype,
                           results=results
                           )


# tag single test case
@app.route('/tag/<inclusionmethod>/<difference>/<filetype>/<browser>')
@demo_mode_check
def tag(inclusionmethod, difference, filetype, browser):
    tasks.run_tagging_single(inclusionmethod, difference, filetype, browser)
    return "Started task of tagging a single result!"



# @app.route('/getelementgroup', methods=['GET','POST'])
# @demo_mode_check
# def getelementgroup():
#     try:
#         return render_template('app/getelementgroup.html')
#     except Exception as e:
#         log('[error]', f"Failed to convert page: {e}")
#         return render_template('error.html', error_message=str(e))  # Return error message
#


@app.route('/sitedetectionresults', methods=['GET','POST'])
@demo_mode_check
def sitedetectionresults():
    try:
        return render_template('app/site_detection_results.html')
    except Exception as e:
        log('[error]', f"Failed to convert page: {e}")
        return render_template('error.html', error_message=str(e))  # Return error message

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/maxredirect')
def maxredirect():
    if request.args.get('n') and request.args.get('url'):
        n = int(request.args.get('n'))
        url = request.args.get('url')

        if url.startswith("http"):
            if n == 0:
                return redirect(url)
            else:
                return redirect(url_for('.index', n=n - 1, url=url), code=302)  # Use code=302 for temporary redirect
        else:
            return "must have http", 400  # Return a 400 error for invalid URL

    return "Ok"


def main():
    app.run(host=BIND_ADDR, port=PORT)


if __name__ == '__main__':
    main()