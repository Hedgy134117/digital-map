function createRoom() {
    window.location = "../room/?admin=true";
}

function joinRoom() {
    let roomId = document.querySelector("input#roomId").value;
    window.location = `../room/?admin=false&id=${roomId}`;
}