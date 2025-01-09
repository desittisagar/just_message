from fastapi import APIRouter, FastAPI, Body, HTTPException, status, WebSocketDisconnect, WebSocket
from message.models import UserModel
from message.services import create_user
from core.database import db
# from main import manager

router = APIRouter()

user_collection = db.get_collection("users")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket}")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                self.disconnect(connection)

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

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{websocket} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Example route
@router.get("/get_message/")
async def read_items():
    # Business logic and message retrieval
    # I am user - 1
    return {"items": ["item1", "item2"]}