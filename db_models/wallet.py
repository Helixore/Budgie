from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from .base import Base

if TYPE_CHECKING:
    from .operations import Operation
    from .household import Household

class Wallet(Base):
    __tablename__ = "Wallets"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    operations: Mapped[List["Operation"]] = relationship(back_populates="wallet")
    
    household_id: Mapped[int] = mapped_column(ForeignKey("Households.id"))
    household: Mapped["Household"] = relationship(back_populates="wallets")