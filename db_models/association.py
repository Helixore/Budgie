from sqlalchemy import Table, Column, ForeignKey
from .base import Base

household_user_association_table = Table(
    "hu_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("Users.id"), primary_key=True),
    Column("household_id", ForeignKey("Households.id"), primary_key=True)
)