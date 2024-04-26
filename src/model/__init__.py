from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

class LoginUser(BaseModel):
    username: str
    password: str

class RegisterUser(BaseModel):
    username: str
    password: str

class UserGroup(BaseModel):
    id: int
    name: str

class CreateGroup(BaseModel):
    name: str
    members_ids: list[int]
