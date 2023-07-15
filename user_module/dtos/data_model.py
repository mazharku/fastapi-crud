from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    name: str
    email: str
    password: str
    items: List[Item]

    class Config:
        orm_mode = True
