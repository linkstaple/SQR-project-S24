from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    token: str


class GroupMember(BaseModel):
    id: int
    username: str
    balance: float


class GroupHistoryEntry(BaseModel):
    timestamp: float
    amount: float
    doer_id: int
    lander_id: int
    payer_ids: list[int]


class Group(BaseModel):
    id: int
    name: str
    members: list[GroupMember]
    history: list[GroupHistoryEntry]


class LoginUser(BaseModel):
    username: str
    password: str


class ListUser(BaseModel):
    id: int
    username: str


class RegisterUser(BaseModel):
    username: str
    password: str


class GroupListItem(BaseModel):
    id: int
    name: str


class GroupList(BaseModel):
    groups: list[GroupListItem]


class CreateGroup(BaseModel):
    name: str
    member_ids: list[int]


class Split(BaseModel):
    group_id: int
    amount: float
    lander_id: int
    payer_ids: list[int]
