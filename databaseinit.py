from mongoengine import Document, StringField, ListField, connect, DynamicDocument, DictField

connect(db="XS-Leaks")
# Data to be stored
class browsers(Document):
    name = StringField(required=True)

class differences(Document):
    name = StringField(required=True)
    response0 = DictField(required=True)
    response1 = DictField(required=True)

class inclusionmethods(Document):
    name = StringField(required=True)
    template = StringField(required=True)


class filetypes(Document):
    name=StringField(required=True)
    contenttype=StringField(required=True)
    filetemplate=StringField(required=True)


class elementgroup(Document):
    url                 = StringField()
    state               = StringField()
    browser             = StringField()
    response            = StringField()
    resources = DictField()




inclusionmethods_datalist=[
        {
            "name": "iframe",
            "template": "iframe.html"
        },
        {
            "name": "iframecsp",
            "template": "iframecsp.html"
        },
        {
            "name": "iframecspreload",
            "template": "iframecspreload.html"
        },
        {
            "name": "iframehashreload",
            "template": "iframehashreload.html"
        },
        {
            "name": "image",
            "template": "image.html"
        },
        {
            "name": "stylesheet",
            "template": "stylesheet.html"
        },
        {
            "name": "object",
            "template": "object.html"
        },
        {
            "name": "script",
            "template": "script.html"
        },
        {
            "name": "embed",
            "template": "embed.html"
        },
        {
            "name": "audio",
            "template": "audio.html"
        },
        {
            "name": "video",
            "template": "video.html"
        },
        {
            "name": "windowopen",
            "template": "windowopen.html"
        },
        {
            "name": "formaction",
            "template": "formaction.html"
        },
        {
            "name": "formactioncsp",
            "template": "formactioncsp.html"
        },
        {
            "name": "fetch",
            "template": "fetch.html"
        },
        {
            "name": "relpreloadscript",
            "template": "relpreloadscript.html"
        },
        {
            "name": "relpreloadstyle",
            "template": "relpreloadstyle.html"
        },
    ]
filetypes_datalist= [
        {
            "name": "html",
            "contenttype": "text/html",
            "filetemplate": "test.html"
        },
        {
            "name": "css",
            "contenttype": "text/css",
            "filetemplate": "test.css"
        },
        {
            "name": "text",
            "contenttype": "text/plain",
            "filetemplate": "test.css"
        },
        {
            "name": "gif",
            "contenttype": "image/gif",
            "filetemplate": "test.gif"
        },
        {
            "name": "wav",
            "contenttype": "audio/wav",
            "filetemplate": "test.wav"
        },
        {
            "name": "pdf",
            "contenttype": "application/pdf",
            "filetemplate": "test.pdf"
        },
        {
            "name": "js",
            "contenttype": "application/javascript",
            "filetemplate": "test.js"
        },
        {
            "name": "json",
            "contenttype": "application/json",
            "filetemplate": "test.json"
        }

    ]
browsers_datalist=["chrome", "firefox", "webkit"]
differences_datalist= [
        {
            "name": "none",
            "response0": {
                "status": 200,
                "headers": []
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name": "timingalloworigin",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Timing-Allow-Origin",
                        "value": "*"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name": "xframeoptions",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "X-Frame-Options",
                        "value": "sameorigin"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"crossoriginresourcepolicy",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Cross-Origin-Resource-Policy",
                        "value": "same-origin"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"csp",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Content-Security-Policy",
                        "value": "default-src 'self';"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"cspframeancestors",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Content-Security-Policy",
                        "value": "frame-ancestors 'self';"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"contentdisposition",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Content-Disposition",
                        "value": "attachment; filename=leak.txt"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"xcontenttypeoptions",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "X-Content-Type-Options",
                        "value": "nosniff"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"crossoriginopenerpolicy",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Cross-Origin-Opener-Policy",
                        "value": "same-origin"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"acceptranges",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Accept-Ranges",
                        "value": "bytes"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name":"cspframeancestorsvsxframeoptions",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Content-Security-Policy",
                        "value": "frame-ancestors 'self';"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": [
                    {
                        "name": "X-Frame-Options",
                        "value": "Deny"
                    }
                ]
            }
        },
        {
            "name": "200vs500",
            "response0": {
                "status": 200,
                "headers": []
            },
            "response1": {
                "status": 500,
                "headers": []
            }
        },
        {
            "name": "redirect",
            "response0": {
                "status": 302,
                "headers": [
                    {
                        "name": "Location",
                        "value": "https://example.com"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name": "refresh0s",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Refresh",
                        "value": "0;url=https://example.com"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name": "refresh1s",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "Refresh",
                        "value": "1;url=https://example.com"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        },
        {
            "name": "testing",
            "response0": {
                "status": 200,
                "headers": [
                    {
                        "name": "X-Connection",
                        "value": "close"
                    },
                    {
                        "name": "Connection",
                        "value": "close"
                    }
                ]
            },
            "response1": {
                "status": 200,
                "headers": []
            }
        }
    ],

datalist = [
    {
        "url": "https://baidu.com/",
        "state": "ano",
        "resources":{
            "inclusionmethods": ["img","object"],
            "domain": ["baidu.com","dss0.bdstatic.com","pss.bdstatic.com","hectorstatic.baidu.com","sp1.baidu.com","sp2.baidu.com","hector.baidu.com"],
            "file": ["index.html",""]
        },
        "response": "<html><body><h1>This is a test page.</h1></body></html>",
        "browser":"chrome"
    },
    {
        "url": "https://www.baidu.com/",
        "state": "visited",
        "resources":{
            "inclusionmethods": ["img", "object"],
            "domain": ["baidu.com", "dss0.bdstatic.com", "pss.bdstatic.com", "hectorstatic.baidu.com", "sp1.baidu.com",
                   "sp2.baidu.com", "hector.baidu.com"],
            "file": ["index.html", ""]
        },

        "response": "<html><body><h1>This is a test page.</h1></body></html>",
        "browser":"chrome"
    },
]

#
# for inclusionmethod in inclusionmethods_datalist:
#     print(inclusionmethod.get('name'))
#     print('\n')
#     inclusionmethods(name=inclusionmethod.get('name'),template=inclusionmethod.get('template')).save()
#
# for filetype in filetypes_datalist:
#     filetypes(name=filetype.get('name'),contenttype=filetype.get('contenttype'),filetemplate=filetype.get('filetemplate')).save()
#
# for browser in browsers_datalist:
#     browsers(name=browser).save()
#
# for difference in differences_datalist:
#     for diff in difference:
#         differences(name=diff.get('name'),response0=diff.get('response0'),response1=diff.get('response1')).save()

for data in datalist:
    print(data)
    elementgroup(url=data.get('url'),resources=data.get('resources'),state=data.get('state'),response=data.get('response'),browser=data.get('browser')).save()