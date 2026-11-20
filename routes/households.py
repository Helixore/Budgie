from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from auth import get_current_active_user
from database import get_session
from db_models.household import Household
from db_models.user import User
from models.household import HouseholdCreate, HouseholdView, HouseholdUpdate


router = APIRouter(prefix="/households")

@router.get("/", tags=["Household", "Read"])
def show_self(current_user: Annotated[User, Depends(get_current_active_user)]) -> List[HouseholdView]:
    with get_session() as session:
        query = select(Household).options(selectinload(Household.users).selectinload(User.details), selectinload(Household.wallets)).where(Household.users.any(User.id == current_user.id) & (Household.disabled == False))
        results = session.execute(query).scalars().all()
        return results
    
@router.post("/create", tags=["Household", "Create"])
def create_household(data: HouseholdCreate, current_user: Annotated[User, Depends(get_current_active_user)]) -> HouseholdView:
    with get_session() as session:
        pq = select(Household).options(selectinload(Household.users)).where((Household.name == data.name) & (Household.users.any(User.id == current_user.id)))
        results = session.execute(pq).scalar_one_or_none()
        if not results:
            newHousehold: Household = Household()
            newHousehold.name = data.name
            newHousehold.users = [current_user]
            session.add(newHousehold)
            session.flush()
            return newHousehold
        else:
            raise HTTPException(status_code=400, detail="Household with a given name already exists")
        
@router.patch("/{household_id}/update", tags=["Household", "Update"])
def update_household(household_id: int, data: HouseholdUpdate, current_user: Annotated[User, Depends(get_current_active_user)]) -> HouseholdView:
    with get_session() as session:
        pq = select(Household).options(selectinload(Household.users)).where((Household.id == household_id) & (Household.users.any(User.id == current_user.id)))
        results = session.execute(pq).scalar_one_or_none()
        if results:
            if data.name:
                results.name = data.name
            session.flush()
            return results
        else:
            raise HTTPException(status_code=404, detail="Household with a given ID not found")       
        
@router.delete("/{household_id}/delete", tags=["Household", "Delete"])
def update_household(household_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> HouseholdView:
    with get_session() as session:
        pq = select(Household).options(selectinload(Household.users)).where((Household.id == household_id) & (Household.users.any(User.id == current_user.id)))
        result = session.execute(pq).scalar_one_or_none()
        if result:
            result.disabled = True
            session.flush()
            return result
        else:
            raise HTTPException(status_code=404, detail="Household with a given ID not found")       