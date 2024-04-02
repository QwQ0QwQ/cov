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

const Ae = (e,t,n)=>new Promise(((s,a)=>{
    n.then(s, a),
    setTimeout(a.bind(null, t), e)
}));


const _e = async e=>{
    let {test_name: n, test_url: s, test_file: a, test_description: o, test_result: i} = e
      , {url0: r, url1: l} = t(s);
    console.log("1231")
    testModalTitel.innerText = n,
    testModalDescription.innerText = o,
    testModalRes0.innerText = i.res0,
    testModalUrl0.href = r,
    testModalUrl0.innerText = r,
    testModalRes1.innerText = i.res1,
    testModalUrl1.href = l,
    testModalUrl1.innerText = l,
    testModalFileLink.href = a,
    testModalFileLink.innerText = a;
    let c = await fetch(a);
    testModalCode.textContent = await c.text(),
    Prism.highlightElement(testModalCode),
    runCustomTestUrl.placeholder = "https?://",
    runCustomTestUrl.value = l,
    runCustomTestResult.innerText = "",
    runCustomTestBtn.onclick = async()=>{
        let t = runCustomTestUrl.value
          , n = "Invalid URL";
        Ee(t) && (runCustomTestBtn.disabled = !0,
        n = await ke(t, e),
        runCustomTestBtn.disabled = !1),
        "" !== runCustomTestResult.innerText && runCustomTestResult.appendChild(document.createElement("hr"));
        let s = document.createElement("div");
        s.innerText = `leak('${t}')\n        -> ${n}`,
        runCustomTestResult.appendChild(s),
        window.WW && window.WW.close()
    }
    ,
    new ge.Modal("#testModal",{
        backdrop: !0
    }).show(),
    location.hash = `${n}`,
    runTestBtn.onclick = async()=>{
        runTestBtn.disabled = !0,
        e.test_result = await ve(e),
        runTestBtn.disabled = !1,
        we(e),
        localStorage.setItem("results", JSON.stringify(Pe("Your Browser", "", ""))),
        testModalRes0.innerText = e.test_result.res0,
        testModalRes1.innerText = e.test_result.res1,
        window.WW && window.WW.close()
    }
}