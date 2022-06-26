import random
import asyncio
import websockets
import datetime
import json

USERS = set()
SERVERS = []
SERVER_IDS = []


async def closeSameAdminServers(admin):
    for server in SERVERS:
        for serverData in server.values():
            if serverData["admin"] == admin:
                SERVERS.remove(server)
                return


async def createServer(admin):
    await closeSameAdminServers(admin)

    serverId = round(random.random() * 10000)
    while serverId in SERVER_IDS:
        serverId = round(random.random() * 10000)
    SERVERS.append({str(serverId): {"admin": admin, "users": set()}})
    SERVER_IDS.append(serverId)
    print(SERVERS)


async def joinServer(serverId, user):
    for server in SERVERS:
        for serverListId in server:
            if serverListId == serverId:
                server[serverListId]["users"].add(user)
                print(SERVERS)
                return


async def main(websocket, path):
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
