from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, Float, Enum, Numeric
from .base import Base
import enum
if TYPE_CHECKING:
    from .wallet import Wallet

class OperationEnum(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"

class Operation(Base):
    __tablename__ = "Operations"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(12,2),default=Decimal("0.00"), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    type: Mapped[OperationEnum] = mapped_column(Enum(OperationEnum, name="operation_enum"), nullable=False)
    
    wallet_id: Mapped[int] = mapped_column(ForeignKey("Wallets.id"))
    wallet: Mapped["Wallet"] = relationship(back_populates="operations")
    