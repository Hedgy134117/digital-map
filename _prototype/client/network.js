let ws = new WebSocket("ws://127.0.0.1:8765/");

ws.onopen = function (e) {
    console.log("Working");
}

ws.onmessage = function (e) {
    console.log(`[SERVER] ${e.data}`);
}

ws.onclose = function (e) {
    console.log(e);
}