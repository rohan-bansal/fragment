window.addEventListener('load', (event) => {
    setBackground();
    grabView();
});

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
