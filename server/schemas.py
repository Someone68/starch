from datetime import datetime

from pydantic import BaseModel
from pydantic.fields import Field


class Register(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    password: str = Field(min_length=8, max_length=256)
    public_key: str


class Login(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    token: str


class KeyOut(BaseModel):
    username: str
    public_key: str
