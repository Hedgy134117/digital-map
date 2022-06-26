import random
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
import pprint
import json

USERS = set()
SERVERS = []
SERVER_IDS = []


async def closeSameAdminServers(admin: WebSocketServerProtocol):
    for server in SERVERS:
        for serverData in server.values():
            if serverData["admin"] == admin:
                SERVERS.remove(server)
                return


async def createServer(admin: WebSocketServerProtocol):
    await closeSameAdminServers(admin)

    serverId = round(random.random() * 10000)
    while serverId in SERVER_IDS:
        serverId = round(random.random() * 10000)
    SERVERS.append({str(serverId): {"admin": admin, "users": []}})
    SERVER_IDS.append(serverId)

    print(f"[createServer] New server created: ID '{serverId}', admin '{admin.id}'")


async def joinServer(serverId: str, user: WebSocketServerProtocol):
    for server in SERVERS:
        for serverListId in server:
            if serverListId == serverId:
                server[serverListId]["users"].append(user)
                print(f"[joinServer] User '{user.id}' joined Server '{serverId}'")
                return


async def main(websocket: WebSocketServerProtocol, path):
    USERS.add(websocket)
    async for message in websocket:
        data = json.loads(message)

        if data["action"] == "createServer":
            await createServer(websocket)
        if data["action"] == "closeServer":
            await closeSameAdminServers(websocket)
        if data["action"] == "joinServer":
            await joinServer(data["serverId"], websocket)


start_server = websockets.serve(main, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
