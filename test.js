(async function () {
    var targetURL = 'https://github.com/';

// get a reference to the requested WindowProxy
    var w = window.open(targetURL);
    var mesg;
// wait until page load (i.e., DOMContentLoaded event)
    setTimeout(() => {
  // side-channel: the number of iframes
    console.log("The page has %d iframes", w.length);
    }, 3000);
    window.addEventListener("message", (evt) => {
  if (evt.origin !== targetURL)
    return;

  /* side-channel: observed messages */
  console.log("captured messages", evt.data)
        mesg=evt.data;
}, false);
    return w.length
})();