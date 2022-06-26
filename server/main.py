import random
import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol
import pprint
import json

USERS = set()
SERVERS = []
SERVER_IDS = []

# Utility Functions
async def getServer(serverId: str) -> dict:
    for server in SERVERS:
        for serverListId in server:
            if serverListId == serverId:
                return server[serverListId]


async def sendMessageToUsers(server: dict, message: str):
    for user in server["users"]:
        await user.send(message)


# Creating and Joining servers
async def createServer(admin: WebSocketServerProtocol):
    serverId = round(random.random() * 10000)
    while serverId in SERVER_IDS:
        serverId = round(random.random() * 10000)
    serverId = str(serverId)
    SERVERS.append(
        {serverId: {"admin": admin, "users": [admin], "names": {admin: str(admin.id)}}}
    )
    SERVER_IDS.append(serverId)

    print(f"[createServer] New server created: ID '{serverId}', admin '{admin.id}'")

    await syncId(serverId)


async def joinServer(serverId: str, user: WebSocketServerProtocol):
    server = await getServer(serverId)
    server["users"].append(user)
    server["names"][user] = str(user.id)

    print(f"[joinServer] User '{user.id}' joined Server '{serverId}'")

    await syncUsers(serverId)
    await syncNames(serverId)
    await syncId(serverId)


# User actions
async def updateName(serverId: str, name: str, user: WebSocketServerProtocol):
    server = await getServer(serverId)
    server["names"][user] = name

    print(f"[updateName] User '{user.id}' set their name to '{name}'")

    await syncNames(serverId)


# Sync State between server & user
async def syncId(serverId: str):
    server = await getServer(serverId)
    message = json.dumps({"type": "id", "id": serverId})

    print(f"[syncId] Sending id to server '{serverId}'")

    await sendMessageToUsers(server, message)


async def syncUsers(serverId: str):
    server = await getServer(serverId)
    userIds = []
    for user in server["users"]:
        userIds.append(str(user.id))

    message = json.dumps({"type": "users", "users": userIds})

    print(f"[syncUsers] Sending users '{userIds}' to server '{serverId}'")

    await sendMessageToUsers(server, message)


async def syncNames(serverId: str):
    server = await getServer(serverId)
    names = []
    for name in server["names"].values():
        names.append(name)
    message = json.dumps({"type": "names", "names": names})

    print(f"[syncNames] Sending names '{names}' to server '{serverId}'")

    await sendMessageToUsers(server, message)


async def main(websocket: WebSocketServerProtocol, path):
    USERS.add(websocket)
    async for message in websocket:
        data = json.loads(message)

        if data["action"] == "createServer":
            await createServer(websocket)
        if data["action"] == "joinServer":
            await joinServer(data["serverId"], websocket)
        if data["action"] == "updateName":
            await updateName(data["serverId"], data["name"], websocket)


start_server = websockets.serve(main, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
