let H = [
    {
    test_name: "Performance API Error Leak",
    test_category: "Status Code",
    test_description: "Detect errors with Performance API.",
    test_file: "/src/leaks/leak_performance_error.js",
    test_function: async e=>{
        let t = document.createElement("script");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name == e)).length;
                return console.debug(`len = ${s}`),
                n(0 !== s ? 0 : 1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "Event Handler Leak (Object)",
    test_category: "Status Code",
    test_description: "Detect errors with onload/onerror with object.",
    test_file: "/src/leaks/leak_eventhandler_object.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("object");
        n.data = e,
        n.onload = e=>(e.target.remove(),
        t(0)),
        n.onerror = e=>(e.target.remove(),
        t(1)),
        document.body.appendChild(n)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "Event Handler Leak (Stylesheet)",
    test_category: "Status Code",
    test_description: "Detect errors with onload/onerror with stylesheet.",
    test_file: "/src/leaks/leak_eventhandler_stylesheet.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("link");
        n.rel = "stylesheet",
        n.href = e,
        n.onload = e=>(e.target.remove(),
        t(0)),
        n.onerror = e=>(e.target.remove(),
        t(1)),
        document.head.appendChild(n)
    }
    ))
}, {
    test_name: "Event Handler Leak (Script)",
    test_category: "Status Code",
    test_description: "Detect errors with onload/onerror with script.",
    test_file: "/src/leaks/leak_eventhandler_script.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("script");
        n.src = e,
        n.onload = e=>(e.target.remove(),
        t(0)),
        n.onerror = e=>(e.target.remove(),
        t(1)),
        document.head.appendChild(n)
    }
    ))
}, {
    test_name: "MediaError Leak",
    test_category: "Status Code",
    test_description: "Detect status codes with MediaError message.",
    test_file: "/src/leaks/leak_mediaerror.js",
    test_function: async e=>{
        let t = document.createElement("audio");
        return new Promise((n=>{
            t.src = e,
            t.onerror = e=>{
                let s = e.target.error.message;
                console.debug(s),
                t.remove(),
                n("Failed to init decoder" === s ? 0 : "500: Internal Server Error" === s ? 1 : s)
                return n
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {

    test_name: "Style Reload Error Leak",
    test_category: "Status Code",
    test_description: "Detect errors with style reload bug.",
    test_file: "/src/leaks/leak_stylereload_error.js",
    test_function: async (e) => {
  return new Promise((t) => {
    let s = document.createElement("iframe");

    // 处理跨域问题
    s.srcdoc = `
        <html>
        <body>
                <script onload="parent.postMessage('', '*')"\n                    src='https://xsinator.com/3sleep'><\/script>
                <style>\n                    @import '${e}';\n                </style>\n                \n        </body>
        </html>`;

    // 等待 iframe 加载完成
    s.onload = () => {
      window.onmessage = async (a) => {
        await n(1e3); // 设置延时计时器1000

        // 捕获异常
        try {
          let o = s.contentWindow.performance.getEntriesByType("resource");
          console.debug(o);
        } catch (err) {
          console.error(err);
          t(0);
          return;
        }

        s.remove();
        let i = o.filter((t) => t.name === e).length;

        return 2 === i ? t(1) : 1 === i ? t(0) : 0 === i ? t(1) : (console.debug(`requests: ${i}`), t(`requests: ${i}`));
      };
    };

    // 5秒超时
    setTimeout(() => {
      s.remove();
      t(0);
    }, 5e3);

    document.body.appendChild(s);
  });
},
    test_timeout: 6e3
}, {

    test_name: "Request Merging Error Leak",
    test_category: "Status Code",
    test_description: "Detect errors with request merging.",
    test_file: "/src/leaks/leak_requestmerging_error.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("iframe");
        window.onmessage = async e=>{
            await s(300);
            let a = n.contentWindow.performance.getEntriesByType("resource").length - 1;
            return n.remove(),
            t(-1 === a ? 1 : a)
        }
        ,
        n.srcdoc = `\n        <html>\n        <body>\n                <script onerror="parent.postMessage('', '*')" \n                    src='${e}'><\/script>\n                <script onload="parent.postMessage('', '*')"\n                    src='${e}'>\n                <\/script>\n        </body>\n        </html>`,
        document.body.appendChild(n)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "CORS Error Leak",
    test_category: "Redirects",
    test_description: "Leak redirect target URL with CORS error.",
    test_file: "/src/leaks/leak_cors_error.js",
    test_function: async e=>fetch(e, {
        credentials: "include",
        mode: "cors"
    }).catch((e=>{
        console.debug(e.message);
        let t = e.message.match(/redirection to (https?:\/\/.*) denied/);
        return t && t[1] ? "https://example.com/?secret#secret" === t[1] ? 1 : t[1] : 0
    }
    ))
}, {
    test_name: "Redirect Start Leak",
    test_category: "Redirects",
    test_description: "Detect cross-origin HTTP redirects by checking redirectStart time.",
    test_file: "/src/leaks/leak_performanceiframe_redirect.js",
    test_function: async e => {
  let t = document.createElement("iframe");
  return t.src = e,
    new Promise((n) => {
      t.onload = t.onerror = async () => {
        t.remove();

        // Check for available Entry before accessing properties:
        const entries = performance.getEntriesByType("resource");
        const matchingEntry = entries.find((t) => t.name === e);

        try {
          if (matchingEntry) {
            // Access properties only if the Entry exists:
            const redirectStatus = matchingEntry.redirectStart === 0 ? 0 : 1;
            n(redirectStatus);
          } else {
            // Handle the case where there's no matching Entry:
            console.warn("No matching resource entry found.");
            n(null); // Or indicate an error with a different value
          }
        } catch (error) {
          console.error("Error handling resource entry:", error);
          n(null); // Or indicate an error with a different value
        }
      };
      document.body.appendChild(t);
    });
}},{
    test_name: "Duration Redirect Leak",
    test_category: "Redirects",
    test_description: "Detect cross-origin redirects by checking the duration.",
    test_file: "/src/leaks/leak_performancefetch_redirect.js",
    test_function: async (e) => {
  return new Promise(async (t) => {
    try {
      // Fetch the resource:
      await fetch(e, {
        mode: "no-cors", // Consider alternative approaches if CORS is needed
        credentials: "include"
      });

      // Wait for a short duration for potential redirects:
      await await a(300);

      // Check for available Entry before accessing properties:
      const entries = performance.getEntriesByType("resource");
      const matchingEntry = entries.find((t) => t.name === e);

      if (matchingEntry) {
        console.debug("Duration: ", matchingEntry.duration);
        t(matchingEntry.duration <= 0 ? 1 : 0); // Reverse logic for easier interpretation
      } else {
        console.warn("No matching resource entry found for:", e);
        // Handle the case where there's no matching Entry (e.g., return a default value)
        t(null); // Or another value indicating an error
      }
    } catch (error) {
      console.error("Error fetching or processing resource:", error);
      t(null); // Or another value indicating an error
    }
  });
}},{
    test_name: "Fetch Redirect Leak",
    test_category: "Redirects",
    test_description: "Detect HTTP redirects with Fetch API.",
    test_file: "/src/leaks/leak_fetch_redirect.js",
    test_function: async e=>fetch(e, {
        credentials: "include",
        mode: "cors",
        redirect: "manual"
    }).then((e=>(console.debug(`res.type = ${e.type}`),
    "opaqueredirect" === e.type ? 1 : void 0))).catch((()=>0))
}, {
    //abc
    test_name: "URL Max Length Leak",
    test_category: "Redirects",
    test_description: "Detect server redirect by abusing URL max length.",
    test_file: "/src/leaks/leak_urlmaxlength.js",
    test_function: async (e) => {
  return new Promise(async (t) => {
    try {
      // Get resource origin using a safer approach:
      const url = new URL(e); // Consider using URL constructor for robust parsing
      const origin = url.origin;

      // Recursive binary search function (adjusted for non-negative count):
      const binarySearch = async (target, low = 0, high = 10000) => {
        if (low >= high) {
          return false; // Not found
        }

        const mid = Math.floor((low + high) / 2);
        const result = await o(i(target, mid));

        if (result === true) {
          return await o(i(target, mid)) ? mid : binarySearch(target, mid + 1, high);
        } else {
          return binarySearch(target, low, mid - 1);
        }
      };

      // Check if the origin is valid using binary search:
      const validOrigin = await binarySearch(origin);

      // Resolve the promise based on the result:
      t(validOrigin ? 0 : 1);

    } catch (error) {
      console.error("Error during origin check:", error);
      t(null); // Or another value indicating an error
    }
  });
},
    test_timeout: 1e4
}, {
    test_name: "Max Redirect Leak",
    test_category: "Redirects",
    test_description: "Detect server redirect by abusing max redirect limit.",
    test_file: "/src/leaks/leak_maxredirectlength.js",
    test_function: async e=>{
        let t = performance.getEntries().length;
        return fetch(`https://127.0.0.1:9876/maxredirect?n=19&url=${encodeURI(e)}`, {
            credentials: "include",
            mode: "no-cors"
        }).then((async e=>(await r(500),
        console.log(`${t} === ${performance.getEntries().length}`),
        t === performance.getEntries().length && 0 !== performance.getEntries().length ? 1 : 0))).catch((e=>1))
    }
    ,
    test_timeout: 6e3
}, {
    test_name: "History Length Leak",
    test_category: "Redirects",
    test_description: "Detect javascript redirects with History API.",
    test_file: "/src/leaks/leak_historylength.js",
    test_function: async e=>new Promise((async t=>{
        await c(window.WW);
        let n = window.WW.history.length;
        return window.WW.location = e,
        await l(2500),
        await c(window.WW),
        console.debug(window.WW.history.length, n),
        window.WW.history.length - n == 3 ? t(1) : t(0)
    }
    )),
    test_timeout: 7e3,
    test_needsWindow: !0
}, {
    test_name: "CSP Violation Leak",
    test_category: "Redirects",
    test_description: "Leak cross-origin redirect target with CSP violation event.",
    test_file: "/src/leaks/leak_csp_blockeduri.js",
    test_function: async t=>new Promise((n=>{
        let s = document.createElement("iframe");
        //添加事件监听器，如果存在csp 重定向返回1
        document.addEventListener('securitypolicyviolation', () => {
        return n(1)
    })
            //否则返回0
        window.onmessage = e=>(s.remove(),n(0)),
        setTimeout((()=>(s.remove(),
        n(0))), 1500),
        s.srcdoc = `<html>\n        <head>\n            <meta http-equiv='Content-Security-Policy' content="default-src * 'unsafe-inline'; connect-src ${e}">\n        </head>\n        <body>\n            <script>\n                document.addEventListener('securitypolicyviolation', e => {parent.postMessage(e.blockedURI, '*')})\n                fetch('${t}', {mode:'no-cors', credentials: 'include'})\n            <\/script>\n        </body>\n        </html>`,
        document.body.appendChild(s)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "CSP Redirect Detection",
    test_category: "Redirects",
    test_description: "Detect cross-origin redirects with CSP violation event.",
    test_file: "/src/leaks/leak_csp_detect.js",
    test_function: async t=>new Promise((n=>{
        let s = document.createElement("iframe");
        window.onmessage = e=>(s.remove(),
        n(1)),
        setTimeout((()=>(s.remove(),
        n(0))), 3e3),
        s.srcdoc = `<html>\n        <head>\n            <meta http-equiv='Content-Security-Policy' content="default-src * 'unsafe-inline'; connect-src ${e}">\n        </head>\n        <body>\n            <script>\n                document.addEventListener('securitypolicyviolation', e => {parent.postMessage(e.blockedURI, '*')})\n                fetch('${t}', {mode:'no-cors', credentials: 'include'})\n            <\/script>\n        </body>\n        </html>`,
        document.body.appendChild(s)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "WebSocket Leak (FF)",
    test_category: "API Usage",
    test_description: "Detect the number of websockets on a page by exausting the socket limit.",
    test_file: "/src/leaks/leak_websocket_ff.js",
    test_function: async(e,t=3e3,n=200)=>{
        let s = "ws://localhost:8000/ff";
        m(s, n),
        await u(500);
        let a = d.length;
        ((e=10)=>{
            for (let t = 0; t < e; t++)
                d.shift().close()
        }
        )(10),
        await u(500),
        window.WW.location = e,
        await u(t),
        m(s, 10),
        await u(400);
        let o = a - d.length;
        return (()=>{
            for (let e of d)
                e.close()
        }
        )(),
        window.WW.location = "about:blank",
        await u(2e3),
        o
    }
    ,
    test_timeout: 8e3,
    test_needsWindow: !0
}, {
    test_name: "WebSocket Leak (GC)",
    test_category: "API Usage",
    test_description: "Detect the number of websockets on a page by exausting the socket limit.",
    test_file: "/src/leaks/leak_websocket_gc.js",
    test_function: async(e,t=2e3,n=255)=>{
        let s = performance.now()
          , a = "ws://localhost:8001/gc";
        console.log("[+] Exausting WS limit until we can not open any new WS.");
        let o = (e=>{
            let t = document.createElement("iframe");
            return t.src = "https://crossorigin.xsinator.xyz/testcases/tests/websocket.php?1",
            document.body.append(t),
            t
        }
        )();
        await h(a, n),
        console.debug(w(), "=", p.length),
        await y(),
        console.debug(w(), "=", p.length),
        console.log("[+] Cannot open any new WS.");
        let i = v(0);
        console.log(`[+] ${i.length} WS are already open.`),
        f(i),
        await g(300),
        console.debug(w(), "=", p.length);
        f(p.slice(0, 10)),
        console.log("[+] Closing 10 ws .."),
        console.debug(w(), "=", p.length),
        console.log(`[+] Opening ${e} in window.`),
        window.WW.location = e,
        await g(t),
        console.log("[+] Checking number of WS."),
        await h(a, 10),
        await y(),
        console.debug(w(), "=", p.length);
        let r = v(0).length;
        return console.log(`[+] ${r} WS on ${e} and ${i.length} WS were already opened.`),
        f(p),
        o.remove(),
        window.WW.location = "about:blank",
        await new Promise((async e=>{
            for (; v(2).length; )
                await g(200);
            return e(1)
        }
        )),
        p = [],
        console.debug(`Took ${performance.now() - s}ms.`),
        r
    }
    ,
    test_timeout: 4e4,
    test_needsWindow: !0
},  {
    test_name: "Frame Count Leak",
    test_category: "Page Content",
    test_description: "Detect the number of iframes on a page.",
    test_file: "/src/leaks/leak_windowlength.js",
    test_function: async e=>new Promise((async t=>(window.WW.location = e,
    await L(500),
    t(window.WW.length)))),
    test_timeout: 4e3,
    test_needsWindow: !0
}, {
    test_name: "Media Dimensions Leak",
    test_category: "Page Content",
    test_description: "Leak dimensions of images or videos.",
    test_file: "/src/leaks/leak_medialeak_dimension.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("img");
        n.src = e,
        n.onload = e=>{
            let n = e.target.naturalHeight
              , s = e.target.naturalWidth;
            return e.target.remove(),
            console.debug(`naturalHeight: ${n}, naturalWidth: ${s}`),
            t(s <= 250 ? 0 : 1)
        }
        ,
        document.body.appendChild(n)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "Media Duration Leak",
    test_category: "Page Content",
    test_description: "Leak duration of audio or videos.",
    test_file: "/src/leaks/leak_medialeak_duration.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("audio");
        n.src = e,
        n.onloadedmetadata = e=>{
            let n = e.target.duration;
            return e.target.remove(),
            console.debug(n),
            t(n < .3 ? 0 : 1)
        }
        ,
        document.body.appendChild(n)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "Performance API Empty Page Leak",
    test_category: "Page Content",
    test_description: "Detect empty responses with Performance API.",
    test_file: "/src/leaks/leak_performance_empty.js",
    test_function: async e=>{
        let t = document.createElement("iframe");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).length;
                return console.debug(`len = ${s}`),
                n(0 !== s ? 0 : 1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "Performance API XSS Auditor Leak",
    test_category: "Page Content",
    test_description: "Detect scripts/event handlers in a page with Performance API.",
    test_file: "/src/leaks/leak_performance_auditor.js",
    test_function: async e=>{
        let t = document.createElement("iframe");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).length;
                return console.debug(`len = ${s}`),
                n(0 !== s ? 0 : 1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "Cache Leak (CORS)",
    test_category: "Page Content",
    test_description: "Detect resources loaded by page. Cache is deleted with CORS error.",
    test_file: "/src/leaks/leak_cache_cors.js",
    test_function: async e=>{
        let t = await (async(e,t="POST")=>{
            let n = 0
              , s = 0;
            for (let s = 0; s < 5; s++)
                await E(e, t),
                await A(100),
                n += await P(e);
            n /= 5,
            await P(e);
            for (let t = 0; t < 5; t++)
                await A(100),
                s += await P(e);
            if (s /= 5,
            console.debug(`avg time nocache: ${n}, avg time cache: ${s}, Limit: ${(n + s) / 2}`),
            n / s < 1.3)
                throw {
                    message: "No timing difference."
                };
            return (n + s) / 2
        }
        )(T, "CORS");
        return new Promise((async n=>{
            await E(T, "CORS");
            let s = document.createElement("iframe");
            s.src = e,
            document.body.append(s),
            await A(1500),
            s.remove();
            let a = await P(T);
            return console.debug(`request took: ${a}, limit is: ${t}`),
            n(a < t ? 1 : 0)
        }
        ))
    }
    ,
    test_timeout: 15e3
}, {
    test_name: "Cache Leak (POST)",
    test_category: "Page Content",
    test_description: "Detect resources loaded by page. Cache is deleted with a POST request.",
    test_file: "/src/leaks/leak_cache_post.js",
    test_function: async e=>{
        let t = await (async(e,t="POST")=>{
            let n = 0
              , s = 0;
            for (let s = 0; s < 5; s++)
                await S(e, t),
                await C(100),
                n += await F(e);
            n /= 5,
            await F(e);
            for (let t = 0; t < 5; t++)
                await C(100),
                s += await F(e);
            if (s /= 5,
            console.debug(`avg time nocache: ${n}, avg time cache: ${s}, Limit: ${(n + s) / 2}`),
            n / s < 1.3)
                throw {
                    message: "No timing difference."
                };
            return (n + s) / 2
        }
        )(x, "POST");
        return new Promise((async n=>{
            await S(x, "POST");
            let s = document.createElement("iframe");
            s.src = e,
            document.body.append(s),
            await C(1500),
            s.remove();
            let a = await F(x);
            return console.debug(`request took: ${a}, limit is: ${t}`),
            n(a < t ? 1 : 0)
        }
        ))
    }
    ,
    test_timeout: 15e3
}, {
    test_name: "Id Attribute Leak",
    test_category: "Page Content",
    test_description: "Leak id attribute of focusable HTML elements with onblur.",
    test_file: "/src/leaks/leak_onblur.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("iframe");
        window.onblur = async()=>(console.debug("onblur fired"),
        window.onblur = "",
        await W(10),
        n.remove(),
        t(1)),
        setTimeout((()=>(window.onblur = "",
        n.remove(),
        t(0))), 1500),
        n.src = `${e}#1337`,
        document.body.appendChild(n)
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "CSS Property Leak",
    test_category: "Page Content",
    test_description: "Leak CSS rules with getComputedStyle.",
    test_file: "/src/leaks/leak_getcomputedstyle.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("link");
        n.rel = "stylesheet",
        n.href = e,
        n.onload = e=>{
            let s = document.createElement("div");
            s.className = "testclassname",
            document.body.appendChild(s);
            let a = window.getComputedStyle(s, null).getPropertyValue("visibility");
            return s.remove(),
            n.remove(),
            t("hidden" === a ? 1 : 0)
        }
        ,
        n.onerror = e=>(n.remove(),
        t(0)),
        document.head.appendChild(n)
    }
    ))
}, {
    test_name: "SRI Error Leak",
    test_category: "HTTP Header",
    test_description: "Leak content length with SRI error.",
    test_file: "/src/leaks/leak_sri_error.js",
    test_function: async e=>fetch(e, {
        credentials: "include",
        mode: "no-cors",
        integrity: "sha256-aaaaa"
    }).catch((e=>{
        console.debug(e.message);
        let t = e.message.match(/Content length: (\d*), Expected content/);
        return t && t[1] ? "221396" === t[1] ? 0 : "917323" === t[1] ? 1 : t[1] : 0
    }
    )),
    test_timeout: 4e3
}, {
    test_name: "ContentDocument X-Frame Leak",
    test_category: "HTTP Header",
    test_description: "Detect X-Frame-Options with ContentDocument.",
    test_file: "/src/leaks/leak_contentdocument.js",
    test_function: async e=>new Promise((async(t,n)=>{
        let s = document.createElement("object");
        return s.data = e,
        document.body.appendChild(s),
        await $(750),
        console.debug(s.contentDocument),
        null !== s.contentDocument ? (s.remove(),
        t(1)) : (s.remove(),
        t(0))
    }
    ))
}, {
    test_name: "Performance API X-Frame Leak",
    test_category: "HTTP Header",
    test_description: "Detect X-Frame-Options with Performance API.",
    test_file: "/src/leaks/leak_performance_xframe.js",
    test_function: async e=>{
        let t = document.createElement("iframe");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).length;
                return console.debug(`len = ${s}`),
                n(0 !== s ? 0 : 1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "Performance API CORP Leak",
    test_category: "HTTP Header",
    test_description: "Detect Cross-Origin-Resource-Policy header with Performance API.",
    test_file: "/src/leaks/leak_performance_corp.js",
    test_function: async e=>{
        let t = document.createElement("img");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).pop();
                return console.debug(`${s}`),
                s ? "" === s.nextHopProtocol ? n(1) : n(0) : n(1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "CORP Leak",
    test_category: "HTTP Header",
    test_description: "Detect Cross-Origin-Resource-Policy header with fetch.",
    test_file: "/src/leaks/leak_fetch_corp.js",
    test_function: async e=>fetch(e, {
        credentials: "include",
        mode: "no-cors"
    }).then((()=>0)).catch((()=>1))
}, {
    test_name: "CORB Leak",
    test_category: "HTTP Header",
    test_description: "Detect X-Content-Type-Options in combination with specific content type using CORB.",
    test_file: "/src/leaks/leak_corb.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("script");
        n.src = e,
        window.addEventListener("error", (e=>(n.remove(),
        console.debug(`window.onerror: ${e.message}`),
        t(0))), {
            once: !0
        }),
        n.onload = n.onerror = async()=>(await N(100),
        n.remove(),
        t(1)),
        document.head.appendChild(n)
    }
    ))
}, {
    test_name: "Download Detection",
    test_category: "HTTP Header",
    test_description: "Detect downloads (Content-Disposition header).",
    test_file: "/src/leaks/leak_download.js",
    test_function: async e=>new Promise((t=>{
        let n = document.createElement("iframe");
        window.onmessage = e=>(n.remove(),
        t(e.data)),
        n.srcdoc = `\n            <iframe id="frame" src="${e}"></iframe>\n            <script>\n                window.onload = () => {\n                    try{\n                        // is it about:blank?\n                        frame.contentWindow.location.href\n                        parent.postMessage(1,'*');\n                    }catch(e){\n                        parent.postMessage(0,'*');\n                    }\n                }\n            <\/script>`,
        document.body.appendChild(n)
    }
    )),
    test_timeout: 6e3
}, {
    test_name: "Performance API Download Detection",
    test_category: "HTTP Header",
    test_description: "Detect downloads (Content-Disposition header) with Performance API.",
    test_file: "/src/leaks/leak_performance_download.js",
    test_function: async e=>{
        let t = document.createElement("iframe");
        return t.src = e,
        new Promise((async n=>{
            document.body.appendChild(t),
            await D(1e3),
            t.remove();
            let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).length;
            return console.debug(`len = ${s}`),
            n(0 !== s ? 0 : 1)
        }
        ))
    }
    ,
    test_timeout: 4e3
}, {
    test_name: "CSP Directive Leak",
    test_category: "HTTP Header",
    test_description: "Detect CSP directives with CSP iframe attribute.",
    test_file: "/src/leaks/leak_csp_directive.js",
    test_function: async(e,t="default-src 'self';")=>new Promise((n=>{
        let s = document.createElement("iframe");
        s.setAttribute("csp", t),
        s.src = e;
        let a = history.length;
        if (a > 48)
            throw new Error("History to long");
        s.onload = ()=>{
            s.onload = ()=>{
                let e = history.length;
                return s.remove(),
                n(e - a)
            }
            ,
            s.src = e
        }
        ,
        document.body.append(s)
    }
    )),
    test_timeout: 3e3
}, {
    test_name: "COOP Leak",
    test_category: "HTTP Header",
    test_description: "Detect Cross-Origin-Opener-Policy header with popup.",
    test_file: "/src/leaks/leak_coop.js",
    test_function: async e=>new Promise((async t=>{
        window.WW.location = e,
        await M(1e3);
        try {
            return console.debug(window.WW.document),
            await M(1e3),
            t(1)
        } catch (e) {
            return console.debug(e),
            await R(window.WW),
            t(0)
        }
    }
    )),
    test_timeout: 4e3,
    test_needsWindow: !0
}];
let t = 0;
// const resultData = JSON.parse('{{ result | safe }}');
// const regex = /\[.+?\]/g;
let resultData = document.getElementById('dataid').getAttribute('d');
resultData=resultData.replace(/\[|\]/g, "")
console.log(resultData)
resultData=resultData.split(",");
const arr = [];
for (const key in resultData) {
  arr.push(resultData[key]);
}
console.log(arr)
leakTable.innerText = "";


const ye = (e,t)=>{
    e.classList.remove("table-success", "table-danger", "table-secondary", "table-warning", "table-default"),
    e.classList.add(`table-${t}`)
}
const we = e=> {
    console.log("resylt:"+e)
    let {test_row: t, test_result: n} = e;
    ye(t, (e => {
            let  n= e;
            let r=""
            if(" 1" == n ||"MEDIA_ELEMENT_ERROR: Format error" == n)
            {
                r="danger"
            }
            else {
                if (" 0" == n || "" == n || "Failed to open media" == n || "Unsupported source type" == n || "No timing difference." === n)
                {
                    r = "success"
                }
                else {
                    if ("no result" == n)
                    {
                        r = "default"
                    }
                    else
                    {
                        if ("Timed Out!" == n)
                        {
                            r = "secondary"
                        }
                        else
                        {
                            if ("string" == typeof n)
                            {
                                console.log("warn")
                                r = "warning"
                            }
                            else
                            {
                                r = "success"
                            }
                        }
                    }
                }
            }
            console.log(n)
            console.log(typeof n)
            console.log(r)
            return r
        }

    )(n))
    // console.log(ye(t, (e => {
    //         let  n= e;
    //         return 1 === n ? "danger" :  void 0 === n || "" === n ? "success" :  "no result" === n ? "default" : "Timed Out!" === n ? "secondary" : "No timing difference." === n ? "success" :  "MEDIA_ELEMENT_ERROR: Format error" === n ? "danger" :  "Failed to open media" === n ||  "Unsupported source type" === n ? "success" : "string" == typeof n ? "warning" : "success"
    //     }
    // )(n)))
}

for (let n of H) {
    let {test_name: e, test_description: s} = n, a = leakTable.insertRow();
    a.insertCell(0).innerText = `${t}`;
    let o = document.createElement("a");
    o.innerText = e, o.href = "#", a.insertCell(1).appendChild(o), a.insertCell(2).innerText = `${s}`,
        // a.onclick = ()=>{
        //     _e(n)
        // }
        // ,
        t++,
        n.test_row = a,
        // console.log(a)
        n.test_result=arr[t]
        we(n)
        // n.test_result ? we(n) : n.test_result = "no result"
}




// const _e = async e=>{
//     let {test_name: n, test_url: s, test_file: a, test_description: o, test_result: i} = e
//       , {url0: r, url1: l} = t(s);
//     testModalTitel.innerText = n,
//     testModalDescription.innerText = o,
//     testModalRes0.innerText = i.res0,
//     testModalUrl0.href = r,
//     testModalUrl0.innerText = r,
//     testModalRes1.innerText = i.res1,
//     testModalUrl1.href = l,
//     testModalUrl1.innerText = l,
//     testModalFileLink.href = a,
//     testModalFileLink.innerText = a;
//     let c = await fetch(a);
//     testModalCode.textContent = await c.text(),
//     Prism.highlightElement(testModalCode),
//     runCustomTestUrl.placeholder = "https?://",
//     runCustomTestUrl.value = l,
//     runCustomTestResult.innerText = "",
//     runCustomTestBtn.onclick = async()=>{
//         let t = runCustomTestUrl.value
//           , n = "Invalid URL";
//         Ee(t) && (runCustomTestBtn.disabled = !0,
//         n = await ke(t, e),
//         runCustomTestBtn.disabled = !1),
//         "" !== runCustomTestResult.innerText && runCustomTestResult.appendChild(document.createElement("hr"));
//         let s = document.createElement("div");
//         s.innerText = `leak('${t}')\n        -> ${n}`,
//         runCustomTestResult.appendChild(s),
//         window.WW && window.WW.close()
//     }
//     ,
//     new ge.Modal("#testModal",{
//         backdrop: !0
//     }).show(),
//     location.hash = `${n}`,
//     runTestBtn.onclick = async()=>{
//         runTestBtn.disabled = !0,
//         e.test_result = await ve(e),
//         runTestBtn.disabled = !1,
//         we(e),
//         localStorage.setItem("results", JSON.stringify(Pe("Your Browser", "", ""))),
//         testModalRes0.innerText = e.test_result.res0,
//         testModalRes1.innerText = e.test_result.res1,
//         window.WW && window.WW.close()
//     }
// }