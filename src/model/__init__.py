from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    token: str


class LoginUser(BaseModel):
    username: str
    password: str


class ListUser(BaseModel):
    id: int
    username: str


class RegisterUser(BaseModel):
    username: str
    password: str


class UserGroup(BaseModel):
    id: int
    name: str


class CreateGroup(BaseModel):
    name: str
    member_ids: list[int]
