from fastapi import APIRouter, FastAPI, Body, HTTPException, status, WebSocketDisconnect, WebSocket
from message.models import UserModel
from fastapi.responses import HTMLResponse
from message.services import create_user
from core.database import db
# from main import manager

router = APIRouter()

user_collection = db.get_collection("users")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/message/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

class ConnectionManager:
    def __init__(self):
        # self.active_connections: list[WebSocket] = []
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        # self.active_connections.append(websocket)
        self.active_connections[client_id] = websocket
        print(f"Client connected {client_id}: {websocket}")

    async def disconnect(self, websocket: WebSocket, client_id):
        del self.active_connections[client_id]
        print(f"Client disconnected {client_id}: {websocket}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for client, connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                # self.disconnect(connection, client_id)

manager = ConnectionManager()

# @router.post("/")

@router.post(
    "/users/",
    response_description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

# Example route
@router.get("/send_message/")
async def create_items():
    # Business logic to send message
    # I am user - 1

    return {"items": ["item1", "item2"]}

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    print("client_id ", client_id)
    try:
        # while True:
        #     data = await websocket.receive_text()
        #     await manager.send_personal_message(f"You wrote: {data}", websocket)
        #     await manager.broadcast(f"Client #{client_id} says: {data}")
        while True:
            print("e43567")
            data = await websocket.receive_text()
            print(data)
            data_ = data.split(":")
            print(data_)
            if len(data_) > 1:
                print("insdie this")
                print("client_id ", client_id)
                a, client, message = data_
                # for connection in manager.active_connections:
                #     print("connection ", connection)
                if client_id == client:
                    print("insdie thisfff1")
                    print(f"You received a message {message}")
                    # await websocket.send_text(f"Message from {client_id}: {data.split(':')[2]}")
                    print(f"Message from {client_id}: {data.split(':')[2]}")
                    # await websocket.send_text(f"to:{client}: {data.split(':')[2]}")
                    break
                else:
                    print("insdie thisfff2")
                    print(f"may be You are sending a message {message}")
                    # await websocket.send_text(f"Message from {client_id}: {data.split(':')[2]}")
                    # await websocket.send_text(f"to:{client}: vdsfe434{data.split(':')[2]}")
                    # for client, connection in manager.active_connections.items():
                    if client in manager.active_connections:
                        if client == client_id:
                            print("found a connection ", client, manager.active_connections[client])
                            await manager.active_connections[client].send_personal_message(f"to:{client}: vdsfe434{data.split(':')[2]}", manager.active_connections[client])
                            break
                # if client == client_id:
                #     print("insdie thisfff")
                #     print(f"You received a message {message}")
            else:
                print("else")
                await manager.send_personal_message(f"You wrote: {data}", websocket)
                await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")

# @router.websocket("/ws/{client_id")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client #{websocket} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)

# Example route
@router.get("/get_message/")
async def read_items():
    # Business logic and message retrieval
    # I am user - 1
    return {"items": ["item1", "item2"]}