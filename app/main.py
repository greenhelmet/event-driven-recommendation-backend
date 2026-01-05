from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/items")
def list_items(limit: int = 10):
    return {"limit": limit}