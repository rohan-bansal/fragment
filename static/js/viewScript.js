window.addEventListener('load', (event) => {
    setBackground();
});

function setBackground() {
    const textbox = $('#displaybox-id').height();
    const background = $('#pattern-bottom').height();

    const screenSection = document.documentElement.clientHeight * 0.25;
    let boxHeight = (textbox - screenSection) + 200;

    $('#pattern-bottom').height(boxHeight + "px");
    // document.getElementById('pattern-bottom')

    // console.log($('pattern-bottom').height());  

}
