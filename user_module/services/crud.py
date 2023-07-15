import logging
from fastapi import Depends
from sqlalchemy.orm import Session

from user_module.data.database import get_db
from user_module.dtos import data_model
from user_module.model import model
from user_module.exceptions.exceptions import UnicornException

logger = logging.getLogger(__name__)


def get_all(db: Session = Depends(get_db)):
    user__all: list = db.query(model.User).all()
    return user__all


def get_by_id(user_id: int, db: Session = Depends(get_db)):
    data = db.query(model.User).filter_by(id=user_id).first()
    user_dto = data_model.UserModel(
        name=data.name,
        email=data.email,
        password="***",
        items=[]
    )
    item_dto = data_model.Item(
        title=data.items.__getitem__(0).title,
        description=data.items.__getitem__(0).description,
        owner_id = data.items.__getitem__(0).owner_id
    )
    user_dto.items = [item_dto]
    return user_dto


def delete_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).get(user_id)
    db.delete(user)
    db.commit()
    return f"user with id {user_id} removed successfully"




def create_user(user: data_model.UserModel, db: Session = Depends(get_db)):
    try:
        db_user = model.User(name=user.name, email=user.email, password=user.password)
        db_item = model.Item(title=user.items.__getitem__(0).title, description=user.items.__getitem__(0).description)
        db_user.items = [db_item]
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return f"user added succesfully with id {db_user.id}"
    except Exception as e:
        logging.error(e)
        raise UnicornException("failed to save db, please check logs for details")


def create_item(user_id: int, item: data_model.Item, db: Session = Depends(get_db)):
    db_item = model.Item(title=item.title, description=item.description, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
