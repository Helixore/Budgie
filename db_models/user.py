from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean
from .base import Base
from .association import household_user_association_table

if TYPE_CHECKING:
    from .household import Household

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean(), default=False, server_default="False")
    details: Mapped["UserDetails"] = relationship(back_populates="user")
    households: Mapped[List["Household"]] = relationship(
        secondary=household_user_association_table, back_populates="users"
    )
    
class UserDetails(Base):
    __tablename__ = "UserDetails"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(String(64), nullable=False)
    lastName: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(12), nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    user: Mapped["User"] = relationship(back_populates="details")