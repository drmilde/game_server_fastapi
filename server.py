from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import uvicorn

class Message(BaseModel):
    m: str

class Entry(BaseModel):
    t: int
    f: int
    b: int    
    m: str

class User(BaseModel):
    id: int
    name: str

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

ticker = 0
users = []
messages = []

current_user = 0
user_ids = [1,2,4,8,16,32,64,128]

async def tick():
    global ticker
    ticker = ticker + 1
    await manager.broadcast(f"tick: {ticker}")

async def addUser(user: User):
    global current_user
    if current_user < 8:
        users.append(user)
        current_user = current_user + 1
    await tick()

def clearUsers():
    global current_user
    current_user = 0
    users.clear()

def getUsers():
    return users

def clearMessages():
    messages.clear()

def resetServer():
    clearUsers()
    clearMessages()

async def addEntry(entry: Entry):
    messages.append(entry)
    await tick()

async def getEntries(id: int):
    # TODO check if message is for id
    result = []
    for entry in messages:
        forme =  entry.t & id
        if (forme):
            result.append(entry)
            entry.t = max(0,entry.t - id)
    tidyMessages()
    await tick()
    return(result)

def tidyMessages():
    global messages
    filtered = [e for e in messages if e.t > 0]
    filtered = [e for e in filtered if (ticker - e.b) < 100]
    messages = filtered
    
app = FastAPI()

@app.get("/")
async def info():
    return {"m": "gs V.01", 
            "commands": ["/j","/l/{id}","/u", "/s/{id}/{r}","/m/{id}", "/c", "/r"]
            }
# User management

@app.get("/j/")
async def join(name:str):
    if current_user < 8:
        user = User(id=user_ids[current_user], name=name)
        await addUser(user)
        return {"id": user.id, "name": name, "m": "joined"}
    else:
        return {"m": "cannot join, max number of users reached"}


@app.get("/l/{id}")
async def leave(id: int):
    return {"id": id, "m": "left"}

@app.get("/u")
async def user_list():
    return {"users": users}

# Message handling

@app.post("/s/{id}/{r}")
async def send(id: int, r:int, m: Message):
    entry = Entry(t=r, f=id, b=ticker, m = m.m)
    await addEntry(entry)
    return {
        "id": id,
        "a": r,
        "m": m.m
    }

@app.get("/m/{id}")
async def message_list(id: int):
    return {
        "id": id,
        "messages": await getEntries(id)
        }

@app.get("/all")
async def all_message_list():
    return {
        "messages": messages
        }

@app.get("/c")
async def clear_messages():
    clearMessages()
    return {"m": "clear messages", "messages": messages}

# Server zurücksetzen

@app.get("/r")
async def reset():
    return {"m": "reset"}

# Websocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Someone said: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1234)