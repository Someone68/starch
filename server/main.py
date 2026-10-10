import base64
import binascii
from sqlite3 import IntegrityError

from auth import DUMMY_HASH, create_token, current_user, hash_password, verify_password
from db import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from models import User
from schemas import KeyOut, Login, Register, TokenOut
from sqlalchemy import select
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)
app = FastAPI(title="starch")


def b64d(value: str, field: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(422, f"{field} is not valid base64")


def b64e(value: bytes) -> str:
    return base64.b64encode(value).decode()


@app.get("/")
async def root(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(f"<h1>Server is running on {request.base_url}</h1>")
    return JSONResponse({"running": True})


@app.get("/check-starch")
async def info():
    return JSONResponse({"version": "0.1.0", "app": "starch"})


@app.post("/register", status_code=201)
def register(body: Register, db: Session = Depends(get_db)):
    public_key = b64d(body.public_key, "public_key")
    if len(public_key) != 32:
        raise HTTPException(422, "public_key must be 32 bytes")

    db.add(
        User(
            public_key=public_key,
            password_hash=hash_password(body.password),
            username=body.username,
        )
    )

    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(409, "username has already been taken")
    db.commit()


@app.post("/login", response_model=TokenOut)
def login(body: Login, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == body.username))
    verified = verify_password(
        user.password_hash if user else DUMMY_HASH, body.password
    )

    if not user or not verified:
        raise HTTPException(401, "invalid username or password")

    return TokenOut(token=create_token(db, user.id))


@app.get("/users/{username}/key", response_model=KeyOut)
def get_public_key(
    username: str, db: Session = Depends(get_db), _: User = Depends(current_user)
):
    user = db.scalar(select(User).where(User.username == username))
    if not user:
        raise HTTPException(404, "user not found")

    return KeyOut(username=user.username, public_key=b64e(user.public_key))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
