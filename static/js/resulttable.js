let t = 0;
// const resultData = JSON.parse('{{ result | safe }}');
// const regex = /\[.+?\]/g;
let id=document.getElementById("id").getAttribute('d');
let resultData =[]
fetch('/api/results/'+id).then(response =>{
    return response.json()
}).then(data =>{
    resultData=data;
    for (let result of resultData) {
    let {test_name: e, test_description: s,test_result:r } = result, a = leakTable.insertRow();
    a.insertCell(0).innerText = `${t}`;
    let o = document.createElement("a");
    o.innerText = e, o.href = "#", a.insertCell(1).appendChild(o), a.insertCell(2).innerText = `${s}`,
        // a.onclick = ()=>{
        //     _e(n)
        // }
        // ,
        t++,
        result.test_row = a,
        // console.log(a)
        we(result)
        // n.test_result ? we(n) : n.test_result = "no result"
}
});
leakTable.innerText = "";
console.log(resultData)

const ye = (e,t)=>{
    e.classList.remove("table-success", "table-danger", "table-secondary", "table-warning", "table-default"),
    e.classList.add(`table-${t}`)
}
const we = e=> {
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
            return r
        }

    )(n))
    // console.log(ye(t, (e => {
    //         let  n= e;
    //         return 1 === n ? "danger" :  void 0 === n || "" === n ? "success" :  "no result" === n ? "default" : "Timed Out!" === n ? "secondary" : "No timing difference." === n ? "success" :  "MEDIA_ELEMENT_ERROR: Format error" === n ? "danger" :  "Failed to open media" === n ||  "Unsupported source type" === n ? "success" : "string" == typeof n ? "warning" : "success"
    //     }
    // )(n)))
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