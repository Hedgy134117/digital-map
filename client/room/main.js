let ws = new WebSocket("ws://127.0.0.1:8765/");
let params = new URLSearchParams(window.location.search);

ws.onopen = function (e) {
    console.log("Working");

    if (params.get("admin") == "true") {
        ws.send(JSON.stringify({ "action": "createServer" }));
    }
    else if (params.get("admin") == "false" && params.get("id") != undefined) {
        ws.send(JSON.stringify({ "action": "joinServer", "serverId": params.get("id") }));
    }
}

// document.querySelector("button").onclick = () => {
//     ws.send(JSON.stringify({ "message": "a" }));
// }

ws.onmessage = function (e) {
    console.log(`[SERVER] ${e.data}`);
}

ws.onclose = function (e) {
    ws.send(JSON.stringify({ "action": "closeServer" }))
}