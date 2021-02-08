let browserType = "";
let enableWebApp = true;

function getBrowser() {
    if (!!window.chrome) {
        browserType = "Chrome";
    }
    else if (typeof InstallTrigger !== 'undefined') {
        browserType = "Firefox";
    }
    else if ((!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0) {
        browserType = "Opera";
    }
    else if (/constructor/i.test(window.HTMLElement) || (!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification))) {
        browserType = "Safari";
    }
    else if (/*@cc_on!@*/false || !!document.documentMode) {
        browserType = "Internet Explorer";
    }
    else if (!window.StyleMedia) {
        browserType = "Edge";
    }
    else if (!!window.CSS0) {
        browserType = "Blink";
    }
    else {
        browserType = "unknown";
    }
}

function browserCheck() {
    getBrowser();
    console.log("Browser: " + browserType);
    let validBrowsers = ["Chrome", "Firefox"];
    if (validBrowsers.indexOf(browserType) === -1) {
        enableWebApp = false;
        let load = $('#load_page');
        setTimeout(function () {
            load.fadeIn(600);
            $('#load_message').html("Incompatible browser detected. Please use Chrome or Firefox to access HMS web applications.");
            return false;
        }, 600);
    }
}

