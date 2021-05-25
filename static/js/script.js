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

function preview() {

    var converter = new showdown.Converter();
    var md = document.getElementById('textarea-note').value;
    var html = converter.makeHtml(md);

    document.getElementById('link-set').innerHTML = html;

    var modal = new tingle.modal({
        footer: true,
        stickyFooter: false,
        closeMethods: ['overlay', 'escape'],
        closeLabel: "Close",
        onClose: () => {
            modal.destroy();
        }
    });

    var stuff = $("#preview-link").html();
    modal.setContent(stuff);
    modal.addFooterBtn('Done', 'tingle-btn tingle-btn--primary', function() {
        modal.close();
    });

    modal.open();
}

function explode() {

    var modal = new tingle.modal({
        footer: true,
        stickyFooter: false,
        closeMethods: ['overlay', 'escape'],
        closeLabel: "Close",
        onClose: () => {
            modal.destroy();
        }
    });

    var stuff = $("#explode-link").html();
    modal.setContent(stuff);
    modal.addFooterBtn('Done', 'tingle-btn tingle-btn--primary', function() {
        modal.close();
    });

    modal.open();
}


function createModal() {

    el = document.getElementById("selector")
    if(el.className == "trigger-True") {
        hash = document.getElementById('hashspan').innerHTML;
        document.getElementById('hashspan').textContent = window.location.hostname + "/" + hash;
        console.log(window.location.hostname, hash)
        document.getElementById('hasha').href = "https://" + window.location.hostname + "/" + hash;
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