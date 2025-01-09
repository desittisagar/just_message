from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from message.api import router as app1_router
from group.api import router as app2_router
from typing import List
# from core.config import settings

app = FastAPI(title="My FastAPI Project", version="1.0.0")

app.include_router(app1_router, prefix="/message")
app.include_router(app2_router, prefix="/group")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)