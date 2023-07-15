from sqlalchemy import Column, INTEGER, String, ForeignKey
from user_module.data.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String)
    password = Column(String)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(INTEGER, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(INTEGER, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
