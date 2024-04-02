from flask import Flask, request, render_template, make_response, jsonify, send_from_directory
from model import elementgroup
from model import browsers
from model import differences
from model import inclusionmethods
from model import filetypes
from model import Testcase
import sys
import os
import json
from functools import wraps
from mongoengine import connect, Document, StringField, ListField, disconnect, DictField
from log import log

PORT = int(os.getenv('PORT', '9876'))
BIND_ADDR = os.getenv('BIND_ADDR', '0.0.0.0')
app = Flask(__name__)
# from werkzeug.middleware.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='.')
app.debug = False



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
    return render_template('app/index.html',
                           browsers=browser,
                           differences=difference,
                           inclusionmethods=inclusionmethod,
                           filetypes=filetype
                           )


@app.route('/faq', methods=['GET'])
def faq():
    inclusionmethod = []
    try:
        inclusionmethods_datalist = inclusionmethods.objects().all()

        for include in inclusionmethods_datalist:
            inclusionmethod.append(include.name)
        log('[init]', "Loading config from MongoDB")
    except Exception as e:
        log('[error]', f"Failed to load config from MongoDB: {e}")
    return render_template('app/faq.html',
                           inclusionmethods=inclusionmethod
                           )



@app.route('/site_detection', methods=['GET'])
def site_detection():
    return render_template('app/site_detection.html',
                           )

@app.route('/blank', methods=['GET'])
def blank():
    return render_template('app/blank.html',)

@app.route('/testing', methods=['GET'])
def testing():
    return render_template('app/testing.html',
                           )

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
        print(browsers.objects.all().count())
        i=0
        for brow in browsers_datalist:
            browser.append(brow.name)
            i+=1
        print("count:")
        print(i)
        for include in inclusionmethods_datalist:
            inclusionmethod.append(include.name)
        for file in filetypes_datalist:
            filetype.append(file.name)
        for diff in differences_datalist:
            difference.append(diff.name)
        print(difference)
        print(inclusionmethod)
        print(filetype)
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



@app.route('/getelementgroup', methods=['GET','POST'])
@demo_mode_check
def getelementgroup():
    try:
        return render_template('app/getelementgroup.html')
    except Exception as e:
        log('[error]', f"Failed to convert page: {e}")
        return render_template('error.html', error_message=str(e))  # Return error message


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/paper.pdf')
def paper():
    return send_from_directory('static', 'autoleak.pdf')


def main():
    connect(db='XS-Leaks')
    app.run(host=BIND_ADDR, port=PORT)


if __name__ == '__main__':
    main()