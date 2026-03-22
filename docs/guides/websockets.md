# WebSocket Support

## Basic WebSocket

```python
from api_toolkit.websocket import WebSocketManager

manager = WebSocketManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

## Authenticated WebSockets

```python
@app.websocket("/ws/secure")
async def secure_ws(websocket: WebSocket, token: str = Query(...)):
    user = await auth.verify_token(token)
    if not user:
        await websocket.close(code=4001)
        return
    # proceed with authenticated connection
```

## Rooms / Channels

```python
manager = WebSocketManager()

@app.websocket("/ws/room/{room_id}")
async def room_ws(websocket: WebSocket, room_id: str, user: User = Depends(auth.current_user)):
    await manager.connect(websocket, user.id, room=room_id)
    async for message in websocket.iter_json():
        await manager.broadcast_to_room(room_id, message, exclude=user.id)
```
