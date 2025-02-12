function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue ? decodeURIComponent(cookieValue) : null;
}

var lastResponseStatus = null
function sendRequest(method, url, data=null, contentType=null, useCSRF=true) {
    let x = new XMLHttpRequest()
    x.onreadystatechange = function() {
    if (x.readyState == XMLHttpRequest.DONE) {
        lastResponseStatus = x.status
    }}
    x.open(method, url)
    if (contentType) {
        x.setRequestHeader('Content-Type', contentType)
    }
    if (useCSRF) {
        x.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    }
    x.send(data)
}
