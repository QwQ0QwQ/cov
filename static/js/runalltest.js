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
    test_function: async e=>new Promise((t=>{
        let s = document.createElement("iframe");
        window.onmessage = async a=>{
            await n(1e3);
            let o = s.contentWindow.performance.getEntriesByType("resource");
            console.debug(o),
            s.remove();
            let i = o.filter((t=>t.name === e)).length;
            return 2 === i ? t(1) : 1 === i ? t(0) : 0 === i ? t(1) : (console.debug(`requests: ${i}`),
            t(`requests: ${i}`))
        }
        ,
        setTimeout((()=>(s.remove(),
        t(0))), 5e3),
        s.srcdoc = `\n        <html>\n        <body>\n                <script onload="parent.postMessage('', '*')"\n                    src='https://xsinator.com/3sleep'><\/script>\n                <style>\n                    @import '${e}';\n                </style>\n                \n        </body>\n        </html>`,
        document.body.appendChild(s)
    }
    )),
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
    test_function: async e=>{
        let t = document.createElement("iframe");
        return t.src = e,
        new Promise((n=>{
            t.onload = t.onerror = ()=>{
                t.remove();
                let s = performance.getEntriesByType("resource").filter((t=>t.name === e)).pop();
                return console.debug(s),
                0 === s.redirectStart ? n(0) : n(1)
            }
            ,
            document.body.appendChild(t)
        }
        ))
    }
}, {
    test_name: "Duration Redirect Leak",
    test_category: "Redirects",
    test_description: "Detect cross-origin redirects by checking the duration.",
    test_file: "/src/leaks/leak_performancefetch_redirect.js",
    test_function: async e=>new Promise((async t=>{
        await fetch(e, {
            mode: "no-cors",
            credentials: "include"
        }),
        await a(300);
        let n = performance.getEntriesByType("resource").filter((t=>t.name === e)).pop();
        return console.debug("Duration: ", n.duration),
        n.duration <= 0 ? t(1) : t(0)
    }
    ))
}, {
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
    test_name: "URL Max Length Leak",
    test_category: "Redirects",
    test_description: "Detect server redirect by abusing URL max length.",
    test_file: "/src/leaks/leak_urlmaxlength.js",
    test_function: async e=>new Promise((async t=>{
        let n = await (async e=>{
            let t = 0
              , n = 1e4
              , s = 0
              , a = !1;
            for (; t < n; )
                s = Math.floor((t + n) / 2),
                a = await o(i(e, s)),
                !1 === a ? n = s - 1 : t = s + 1;
            return a = await o(i(e, t)),
            !1 === a && t--,
            a = await o(i(e, t)),
            !1 === a ? (console.debug("Error after last check !!!"),
            0) : (console.debug(`DONE: length: ${t}, result: ${a}`),
            t)
        }
        )((e=>{
            let t = document.createElement("a");
            return t.href = e,
            t.origin
        }
        )(e) + "/testcases/tests/blank.php");
        return t(await o(i(e, n - 3)) ? 0 : 1)
    }
    )),
    test_timeout: 1e4
}, {
    test_name: "Max Redirect Leak",
    test_category: "Redirects",
    test_description: "Detect server redirect by abusing max redirect limit.",
    test_file: "/src/leaks/leak_maxredirectlength.js",
    test_function: async e=>{
        let t = performance.getEntries().length;
        return fetch(`https://xsinator.com/testcases/files/maxredirect.php?n=19&url=${encodeURI(e)}`, {
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
        window.onmessage = e=>(s.remove(),
        "https://example.com" === e.data ? n(1) : t.includes(e.data) ? n(0) : n(e.data)),
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
        let s = "wss://xsinator.com/5sleep";
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
          , a = "wss://xsinator.com/ws";
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
}, {
    test_name: "Payment API Leak",
    test_category: "API Usage",
    test_description: "Detect if another tab is using the Payment API.",
    test_file: "/src/leaks/leak_payment.js",
    test_function: async e=>new Promise((async t=>{
        if (!window.PaymentRequest)
            return t("PaymentRequest not supported.");
        window.WW.location = e,
        await k(2e3);
        let n = new PaymentRequest(b,_);
        n.show().catch((e=>"Another PaymentRequest UI is already showing in a different tab or window." == e.message ? t(1) : t(0))),
        n.abort()
    }
    )),
    test_timeout: 5e3,
    test_needsWindow: !0
}, {
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

runCustomTestUrl.placeholder = "https?://",
runAllTests.onclick = async e=>{
    console.log("click")
    Se(),
    Fe(),
    be();
    let t = runAllTests.innerHTML;
    let u = runCustomTestUrl.value
          , n = "Invalid URL";
    Ee(u) && (runAllTests.disabled = !0,
        runAllTests.disabled = !1),
    runAllTests.innerText = "Running ...",
    window.WW = Te();
    for (let e of H)
        // console.log(e)
        e.test_result =await ke(u, e),
            console.log(e.test_result)
        we(e);
    Se(),
    runAllTests.innerHTML = t,
    exportToServer("https://127.0.0.1:8000/"),
    window.WW.close(),
    localStorage.setItem("results", JSON.stringify(Pe("Your Browser", "", ""))),
    compareResultsBtn.disabled = !1
}


//浏览器全部测试
const ve = async e=>{
    let n, s, {test_name: a, test_url: o, test_function: i, test_row: r, test_timeout: l, test_needsWindow: c} = e;
    // ye(r, "secondary");
    let {url0: d, url1: u} = t(o);
    l || (l = 5e3),
    c && (window.WW && !window.WW.closed || (window.WW = Te()));
    try {
        n = await Ae(l, new Error("Timed Out!"), i(d))
    } catch (e) {
        console.log(`Error running ${a} for ${d}`),
        console.log(e),
        n = e.message
    }
    try {
        s = await Ae(l, new Error("Timed Out!"), i(u))
    } catch (e) {
        console.log(`Error running ${a} for ${u}`),
        console.log(e),
        s = e.message
    }
    return {
        res0: n,
        res1: s
    }
}
const ye = (e,t)=>{
    e.classList.remove("table-success", "table-danger", "table-secondary", "table-warning", "table-default"),
    e.classList.add(`table-${t}`)
}

const Te = ()=>window.open("/blank", "targetWindow", `toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=yes,left=${screen.width - 250},width=250,height=250`)

const Ae = (e,t,n)=>new Promise(((s,a)=>{
    n.then(s, a),
    setTimeout(a.bind(null, t), e)
}
))


const Ee = e=>{
    let t = document.createElement("input");
    return t.type = "url",
    t.value = e,
    !(!t.checkValidity() || !e.startsWith("http"))
};


const ke = async(e,t)=>{
    let n, {test_name: s, test_function: a, test_timeout: o, test_needsWindow: i} = t, r = e;
    o || (o = 5e3),
    i && (window.WW && !window.WW.closed || (window.WW = Te()));
    try {
        n = await Ae(o, new Error("Timed Out!"), a(r))
    } catch (e) {
        console.log(`Error running ${s} for ${r}`),
        console.log(e),
        n = e.message
    }
    return n
};


const we = e=>{
    let {test_row: t, test_result: n} = e;
    ye(t, (e=>{
        let {res0: t, res1: n} = e;
        return 0 === t && 1 === n ? "danger" : void 0 === t || void 0 === n || "" === t || "" === n ? "success" : "no result" === t && "no result" === n ? "default" : "Timed Out!" === t && "Timed Out!" === n ? "secondary" : "PaymentRequest not supported." === t && "PaymentRequest not supported." === n || "No timing difference." === t || "No timing difference." === n ? "success" : "DEMUXER_ERROR_COULD_NOT_OPEN: FFmpegDemuxer: open context failed" === t && "MEDIA_ELEMENT_ERROR: Format error" === n ? "danger" : "Failed to open media" === t && "Failed to open media" === n || "Unsupported source type" === t && "Unsupported source type" === n ? "success" : "string" == typeof t || "string" == typeof n ? "warning" : "success"
    }
    )(n))
}


const Se = ()=>{
    runAllTests.disabled ? runAllTests.disabled = !1 : runAllTests.disabled = !0
    // exportResultsBtn.disabled ? exportResultsBtn.disabled = !1 : exportResultsBtn.disabled = !0
}

const Fe = (e=navigator.userAgent)=>{
    appVersionField.innerText = e
}



const be=()=>{
	for(let e of H)e.test_result={
		res0:"no result",res1:"no result"}
	,e.test_row&&ye(e.test_row,"default")}