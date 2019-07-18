/*
   Open a new tab, and load "main.html" into it.
 */
function openMainPage(tab) {
    browser.tabs.create({
        "url": "http://localhost:8080/?url="+encodeURIComponent(tab.url)
    });
}

/*
   Add openMainPage() as a listener to clicks on the browser action.
 */
browser.browserAction.onClicked.addListener(openMainPage);
