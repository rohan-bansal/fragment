var explodeModal = "";

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

    explodeModal = new tingle.modal({
        footer: true,
        stickyFooter: false,
        closeMethods: ['overlay', 'escape'],
        closeLabel: "Close",
        onClose: () => {
            explodeModal.destroy();
        }
    });

    var stuff = $("#explode-link").html();
    explodeModal.setContent(stuff);


    explodeModal.open();
}

$(document).on("submit", "#explosion", (e) => {
    if(!$('input[name="eType"]:checked').val()) {
        
    } else {
        const element = $('input[name="eType"]:checked').parent().find("input").eq(1);

        if(element.hasClass('custom-input')) {
            if(element.val() <= 0) {
                e.preventDefault();
                Swal.fire({
                    title: 'Error!',
                    text: 'Invalid field: Cannot be null, negative, or zero.',
                    icon: 'error',
                });
                return;
            } else {
                document.getElementById('does-it-explode').value = $('input[name="eType"]:checked').val();
                document.getElementById('does-it-explode-input').value = element.val();
                document.getElementById('explode-enabled').style.display = "block";
            }
        } else {
            document.getElementById('does-it-explode').value = $('input[name="eType"]:checked').val();
            document.getElementById('explode-enabled').style.display = "block";
        }
    }

    e.preventDefault();
    explodeModal.close();
   
});

function disableExplode() {
    document.getElementById('does-it-explode').value = "none";
    document.getElementById('does-it-explode-input').value = "none";
    document.getElementById('explode-enabled').style.display = "none";
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