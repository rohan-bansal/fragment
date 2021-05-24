window.addEventListener('load', (event) => {
    setBackground();
});

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
