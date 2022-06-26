let ws = new WebSocket("ws://127.0.0.1:8765/");
let params = new URLSearchParams(window.location.search);
let isAdmin = params.get("admin") == "true";
let serverId = params.get("id");

ws.onopen = function (e) {
    console.log("Working");

    if (isAdmin) {
        ws.send(JSON.stringify({ "action": "createServer" }));
    }
    else if (serverId != undefined) {
        ws.send(JSON.stringify({ "action": "joinServer", "serverId": serverId }));
    }
}

ws.onmessage = function (e) {
    console.log(`[SERVER] ${e.data}`);
    let data = JSON.parse(e.data);
    switch (data["type"]) {
        case "id":
            updateId(data["id"]);
            break;
        case "users":
            updateUsers(data["users"]);
            break;
    }
}

ws.onclose = function (e) {
    ws.send(JSON.stringify({ "action": "closeServer" }))
}

function updateUsers(users) {
    document.querySelector("#users").innerText = users;
}

function updateId(id) {
    document.querySelector("#id").innerText = id;
}