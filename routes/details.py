from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from auth import get_current_active_user
from db_models.user import User, UserDetails
from models.user import UserDetailsCreate, UserDetailsView
from database import get_session

router = APIRouter(prefix="/details")

@router.post("/add", tags=["User", "Details"])
def details_add(data: UserDetailsCreate, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserDetailsView:
    with get_session() as session:
        uq = select(UserDetails).where(UserDetails.user_id == current_user.id)
        result = session.execute(uq).scalar_one_or_none()
        if result:
            #update - redirect or throw HTTPException
            raise HTTPException(status_code=400, detail="Detailed info of user already exists")
            pass
        else:
            userDetails: UserDetails = UserDetails()
            userDetails.firstName = data.firstName
            userDetails.lastName = data.lastName
            userDetails.email = data.email
            userDetails.phone = data.phone
            userDetails.user = current_user
            userDetails.user_id = current_user.id
            session.add(userDetails)
            session.flush()
            return userDetails