var count = 30000;
var offset;
var counter;

window.addEventListener('load', (event) => {
    setBackground();
    // grabView();
    tippy('.tooltip-firstview', {
        animation: 'shift-away',
        inertia: true,
        animateFill: true,
        theme: "bettertext",
    });
    checkExplodeType();
    // enableDeleteModal();
});

function timer() {
    if (count <= 0) {
        deleteRecord();
        document.getElementById("countdown").innerHTML = "0";
        localStorage.removeItem('countdown-session');
        clearInterval(counter);
        return;
    }
    count -= delta();
    sessionStorage.setItem('countdown-session', count);
    displayCount(count);
}

function delta() {
    var now = Date.now(),
        d   = now - offset;

    offset = now;
    return d;
}

function displayCount(count) {
    var res = (count / 1000);
    document.getElementById("countdown").innerHTML = res.toPrecision(count.toString().length - 1);
}

function deleteRecord() {
    $.post( "/" + window.location.pathname.replace(/^\/([^\/]*).*$/, '$1'), {
    });
    window.location.reload();
}

function checkExplodeType() {
    const ele = document.getElementById("explode-enabled-30sec");
    if(ele) {
        var sess = sessionStorage.getItem('countdown-session');
        if (sess) {
            count = sess;
        }
        clearInterval(counter);
        offset   = Date.now();
        counter = setInterval(timer, 10);
    }
}

function grabView() {
    $.get('https://www.cloudflare.com/cdn-cgi/trace', function(data) {
    data = data.trim().split('\n').reduce(function(obj, pair) {
        pair = pair.split('=');
        return obj[pair[0]] = pair[1], obj;
    }, {});
    console.log(data['ip']);
    });

    $.getJSON('https://json.geoiplookup.io/?callback=?', function(data) {
        console.log(JSON.stringify(data, null, 2));
    });
}


function setBackground() {
    const textbox = $('#displaybox-id').height();
    const background = $('#pattern-bottom').height();

    const screenSection = document.documentElement.clientHeight * 0.25;
    const screenHalf = document.documentElement.clientHeight * 0.50;
    let boxHeight = (textbox - screenSection) + 200;

    const bounding = document.querySelector('#displaybox-id').getBoundingClientRect();
    if (bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)) {
        boxHeight = screenHalf;
    }


    $('#pattern-bottom').height(boxHeight + "px");


}

function enableDeleteModal() {
    var del = new tingle.modal({
        footer: true,
        stickyFooter: false,
        closeMethods: ['overlay', 'escape'],
        closeLabel: "Close",
        onClose: () => {
            del.destroy();
        }
    });

    var stuff = $("#delete-link").html();
    del.setContent(stuff);


    del.open();
}