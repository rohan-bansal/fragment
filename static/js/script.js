(function() {

}).call(this);

// function printElement(element) {
//     var elem = document.getElementById(element);

//     const newDiv = document.createElement("div");
//     const newContent = document.createTextNode(elem.value);

//     newDiv.appendChild(newContent);

//     // newDiv.style.display = "none";
//     newDiv.id = "temp-text";
//     document.getElementById('pattern-div').insertBefore(newDiv, document.getElementById('temp'))

//     printJS('temp-text', 'html')

//     newDiv.style.display = "none";
//     newDiv.parentNode.removeChild(newDiv);
// }


function validateTextArea() {
    var x = document.forms["note-body"]["textarea-note"].value;
    if (x == "") {
        Swal.fire({
            title: 'Error!',
            text: 'Write something first!',
            icon: 'error',
            })
      return false;
    }
    return true;
}

window.addEventListener('load', (event) => {
    createModal();
});


function createModal() {

    el = document.getElementById("selector")
    if(el.className == "trigger-True") {
        hash = document.getElementById('hashspan').innerHTML;
        document.getElementById('hashspan').textContent = window.location.hostname + "/" + hash;
        document.getElementById('hasha').href = window.location.hostname + "/" + hash;
        var modal = new tingle.modal({
            footer: true,
            stickyFooter: false,
            closeMethods: ['overlay', 'escape'],
            closeLabel: "Close",
            onClose: () => {
                modal.destroy();
            }
        });
    
        var stuff = $("#modal-link").html();
        modal.setContent(stuff);
        modal.addFooterBtn('Awesome!', 'tingle-btn tingle-btn--primary', function() {
            modal.close();
        });
    
        modal.open();
    }
}