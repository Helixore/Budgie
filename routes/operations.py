from typing import Annotated, Union, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from auth import get_current_active_user
from db_models.household import Household
from db_models.user import User
from db_models.wallet import Wallet
from db_models.operations import Operation
from models.operations import OperationCreate, OperationView
from database import get_session

router = APIRouter(prefix="/operations")

@router.get("/", tags=["Operations", "Read"])
def read_operations(current_user: Annotated[User, Depends(get_current_active_user)]) -> List[OperationView]:
    with get_session() as session:
        oq = (
            select(Operation)
                .options(
                    selectinload(Operation.wallet).selectinload(Wallet.household).selectinload(Household.users), 
                    )
            .where(
                Operation.wallet.has(
                    Wallet.household.has(
                        Household.users.any(User.id == current_user.id)
                            )
                        )
                    )
                )
        results = session.execute(oq).scalars().all()
        return results


@router.get("/{operation_id}", tags=["Operations", "Read"])
def read_operation(operation_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> OperationView:
    with get_session() as session:
        oq = (
            select(Operation)
                .options(
                    selectinload(Operation.wallet).selectinload(Wallet.household).selectinload(Household.users), 
                    )
            .where(
                (Operation.wallet.has(
                    Wallet.household.has(
                        Household.users.any(User.id == current_user.id)
                            )
                        )
                    ) &
                (Operation.id == operation_id)
            )
            )
        result: Operation = session.execute(oq).scalar_one_or_none()
        if result:
            return result
        else:
            raise HTTPException(404, "Operation with given ID doesn't exist.")
        
@router.post("/create", tags=["Operations", "Create"])
def create_operation(data: OperationCreate, current_user: Annotated[User, Depends(get_current_active_user)]) -> OperationView:
    with get_session() as session:
        wq = (select(Wallet).options(
            selectinload(Wallet.household).selectinload(Household.users), 
            selectinload(Wallet.operations))
            .where(
                (Wallet.household.has(
                    Household.users.any(User.id == current_user.id)
                )) &
                (Wallet.id == data.wallet_id)
            )
        )
        result: Wallet = session.execute(wq).scalar_one_or_none()
        if result:
            newOperation: Operation = Operation()
            newOperation.name = data.name
            newOperation.value = data.value
            newOperation.currency = data.currency
            newOperation.type = data.type
            newOperation.wallet_id = result.id
            newOperation.wallet = result
            session.add(newOperation)
            session.flush()
            return newOperation
        else:
            raise HTTPException(404, "Wallet with given ID wasn't found.")