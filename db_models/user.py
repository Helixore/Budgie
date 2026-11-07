from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean
from db_models.base import Base

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean(), default=False, server_default="False")
    details: Mapped["UserDetails"] = relationship(back_populates="user")
    
class UserDetails(Base):
    __tablename__ = "UserDetails"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(String(64), nullable=False)
    lastName: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(12), nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    user: Mapped["User"] = relationship(back_populates="details")