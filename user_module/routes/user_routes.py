from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from user_module.data.database import get_db
from user_module.dtos import data_model
from user_module.services import crud as service

router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)


@router.get("/name")
def return_name():
    return {"name": "John Doe"}


@router.get("")
async def fetch_all(db: Session = Depends(get_db)):
    return service.get_all(db)


@router.get("/{user_id}")
async def fetch_by_id(user_id: int, db: Session = Depends(get_db)):
    return service.get_by_id(user_id, db)


@router.delete("/{user_id}")
async def delete_by_id(user_id: int, db: Session = Depends(get_db)):
    return service.delete_by_id(user_id, db)


@router.post("")
def create_user(user: data_model.UserModel, db: Session = Depends(get_db)):
    return service.create_user(user, db)


@router.post("/item/{user_id}")
def create_item(user_id: int, item: data_model.Item, db: Session = Depends(get_db)):
    return service.create_item(user_id, item, db)
