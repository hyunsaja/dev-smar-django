document.addEventListener('click', function(event) {
    if (event.target.id.toUpperCase().includes("submit".toUpperCase()))
    submitAction(event.target);
});

function submitAction(eventObj) {  
    // ---------------------------------------
    let method = eventObj.getAttribute("data-method").toUpperCase();
    let enctype = eventObj.getAttribute("data-enctype");
    let action = eventObj.getAttribute("data-action");
    let innerhtml = document.getElementById(eventObj.getAttribute("data-innerhtml-id"));
    let option = eventObj.getAttribute("data-option");
    // ---------------------------------------
    if(!method) {
        alert("ERROR: FORM data-method UNDEFINED");
        return;
    }
    if(!action) {
        alert("ERROR: FORM data-action UNDEFINED");
        return;
    }
    if(!innerhtml) {
        alert("ERROR: FORM data-innerhtml-id UNDEFINED");
        return;
    }
    // ---------------------------------------
    let form = eventObj.closest("form");
    if(!form){
        form = document.createElement("form");
        method = 'GET';
    }

    let formData = new FormData(form);
    eventObj.setAttribute("disabled", true);

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {    
        if (this.readyState == xhttp.DONE && this.status == 200) {    
            innerhtml.innerHTML = this.responseText;    
        }
        eventObj.removeAttribute("disabled");
    };

    xhttp.open(method, action, true);
    xhttp.send(formData)
}