from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from .base import Base
from .association import household_user_association_table

if TYPE_CHECKING:
    from .user import User
    from .wallet import Wallet



class Household(Base):
    __tablename__ = "Households"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    users: Mapped[List["User"]] = relationship(
        secondary=household_user_association_table, back_populates="households"
    )
    wallets: Mapped[List["Wallet"]] = relationship(back_populates="household")
    
