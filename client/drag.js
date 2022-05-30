function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text");
    let el = document.getElementById(data)
    ev.target.appendChild(el);

    for (let element of board.elements) {
        if (element.text == el.id) {
            board.moveElement(element)
        }
    }

}