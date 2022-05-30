class Element {
    constructor(x, y, text) {
        this.x = x;
        this.y = y;
        this.text = text;
    }

    generateHTML() {
        this.dom = document.createElement("div");
        this.dom.innerText = this.text;
        this.dom.setAttribute("draggable", "true");
        this.dom.setAttribute("ondragstart", "drag(event)");
        this.dom.setAttribute("id", this.text);
    }
}