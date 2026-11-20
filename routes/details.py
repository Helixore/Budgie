from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from auth import get_current_active_user
from db_models.user import User, UserDetails
from models.user import UserDetailsCreate, UserDetailsView, UserDetailsUpdate
from database import get_session

router = APIRouter(prefix="/details")

@router.post("/add", tags=["Details", "Create"])
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
        
@router.patch("/update", tags=["Details", "Update"])
def details_update(data: UserDetailsUpdate, current_user: Annotated[User, Depends(get_current_active_user)]) -> UserDetailsView:
    with get_session() as session:
        uq = select(UserDetails).where(UserDetails.user_id == current_user.id)
        result = session.execute(uq).scalar_one_or_none()
        if not result:
            #update - redirect or throw HTTPException
            raise HTTPException(status_code=404, detail="Detailed info of user not found")
            pass
        else:
            if data.firstName:
                result.firstName = data.firstName
            if data.lastName:
                result.lastName = data.lastName
            if data.email:
                result.email = data.email
            if data.phone:
                result.phone = data.phone
            session.flush()
            return result