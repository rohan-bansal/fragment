var count = 30000;
var offset;
var counter;

function formatForDisplay(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    var month = date.toLocaleString('default', { month: 'short' });
    var day = date.getDate();
    year = date.getFullYear();
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return [strTime, month + " " + day + ", " + year];
}

window.addEventListener('load', (event) => {
    setBackground();
    tippy('.tooltip-firstview', {
        animation: 'shift-away',
        inertia: true,
        animateFill: true,
        theme: "bettertext",
    });
    checkExplodeType();
});

function timer() {
    if (count <= 0) {
        deleteRecord();
        document.getElementById("countdown").innerHTML = "0";
        sessionStorage.removeItem('countdown-session');
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
        count = 30000
        clearInterval(counter);
        offset   = Date.now();
        counter = setInterval(timer, 10);
    }
    const ele2 = document.getElementById("explode-enabled-xsec");
    if(ele2) {
        var sess = sessionStorage.getItem('countdown-session');
        if (sess) {
            count = sess;
        }
        count = parseInt(document.getElementById("countdown").innerHTML) * 1000;
        clearInterval(counter);
        offset   = Date.now();
        counter = setInterval(timer, 10);
    }
    const ele3 = document.getElementById("explode-enabled-xviews");
    if(ele3) {
        $.get('https://www.cloudflare.com/cdn-cgi/trace', function(data) {
            data = data.trim().split('\n').reduce(function(obj, pair) {
                pair = pair.split('=');
                return obj[pair[0]] = pair[1], obj;
            }, {});
            $.ajax({
                type: 'POST',
                url: '/content/viewcounter',
                dataType: 'json',
                contentType: 'application/json; charset=UTF-8',
                data: JSON.stringify({
                    "ip" : data['ip']
                }),
            });
        });   
    }
    const ele4 = document.getElementById("explode-enabled-xhour");
    if(ele4) {
        const time = document.getElementById("utc-server-time").innerHTML;
        
        const date = new Date(time);
        const localDate = formatForDisplay(date);

        document.getElementById("et-time").innerHTML = localDate[0]
        document.getElementById("et-date").innerHTML = localDate[1]
    }
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