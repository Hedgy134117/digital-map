class Board {
    constructor(width, height) {
        this.dom = document.body.querySelector("main");
        this.width = width;
        this.height = height;
        this.elements = [];
    }

    generateHTML() {
        for (let w = 0; w < this.width; w++) {
            let currentCol = document.createElement("div");
            currentCol.setAttribute("class", "col");
            this.dom.appendChild(currentCol);
            for (let h = 0; h < this.height; h++) {
                let currentEl = document.createElement("div");
                currentEl.setAttribute("class", "el");
                currentEl.setAttribute("ondrop", "drop(event)");
                currentEl.setAttribute("ondragover", "allowDrop(event)");
                currentCol.appendChild(currentEl);
            }
        }
    }

    addElement(element) {
        this.elements.push(element);
        element.generateHTML();
        this.dom.children[0].children[0].appendChild(element.dom);
    }

    moveElement(element) {
        for (let x = 0; x < this.width; x++) {
            if (this.dom.children[x] == element.dom.parentElement.parentElement) {
                for (let y = 0; y < this.height; y++) {
                    if (this.dom.children[x].children[y] == element.dom.parentElement) {
                        element.x = x;
                        element.y = y;
                    }
                }
            }
        }
    }
}