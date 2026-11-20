from typing import Annotated, Union, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from auth import get_current_active_user
from db_models.household import Household
from db_models.user import User
from db_models.wallet import Wallet
from models.wallet import WalletView, WalletCreate, WalletUpdate
from database import get_session

router = APIRouter(prefix="/wallets")

@router.get("/", tags=["Wallet", "Read"])
def show_self(current_user: Annotated[User, Depends(get_current_active_user)]) -> List[WalletView]:
    with get_session() as session:
        wq = (select(Wallet).options(
            selectinload(Wallet.household).selectinload(Household.users), 
            selectinload(Wallet.operations))
            .where(
                Wallet.household.has(
                    Household.users.any(User.id == current_user.id)
                )
            )
        )
        results = session.execute(wq).scalars().all()
        return results
@router.get("/{wallet_id}", tags=["Wallet", "Read"])
def show_wallet_id(wallet_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> WalletView:
    with get_session() as session:
        wq = (select(Wallet)
              .options(
                selectinload(Wallet.household).selectinload(Household.users), 
                selectinload(Wallet.operations))
              .where(
                  (Wallet.id == wallet_id) & 
                  (Wallet.household.has(
                        Household.users.any(User.id == current_user.id)
                    )))
            )
        result: Wallet = session.execute(wq).scalar_one_or_none()
        if result:
            return result
        else:
            raise HTTPException(404, "Wallet with given ID not found.")

@router.post("/create", tags=["Wallet", "Create"])
def create_wallet(data: WalletCreate, current_user: Annotated[User, Depends(get_current_active_user)]) -> WalletView:
    with get_session() as session:
        hq = (select(Household)
                .options(
                    selectinload(Household.users),
                    selectinload(Household.wallets)
                )
                .where(
                    Household.id == data.household_id
                )
            )
        result: Household = session.execute(hq).scalar_one_or_none()
        if result:
            newWallet = Wallet()
            newWallet.name = data.name
            newWallet.operations = []
            newWallet.disabled = False
            newWallet.household = result
            newWallet.household_id = result.id
            session.add(newWallet)
            session.flush()
            return newWallet
        else:
            raise HTTPException(404, "Household with given ID not found.")

@router.patch("/{wallet_id}/update", tags=["Wallet", "Update"])
def update_wallet(wallet_id: int, data: WalletUpdate, current_user: Annotated[User, Depends(get_current_active_user)]) -> WalletView:
    with get_session() as session:
        wq = (select(Wallet)
                .options(
                    selectinload(Household.users).selectinload(Household.users),
                    selectinload(Household.wallets)
                )
              .where(
                  (Wallet.id == wallet_id) &
                  (Wallet.household.has(
                        Household.users.any(User.id == current_user.id)
                    )
                  )
              )
        )
        result: Wallet = session.execute(wq).scalar_one_or_none()
        if result:
            if data.name:
                result.name = data.name
            session.flush()
            return result
        else:
            raise HTTPException(404, "Wallet with given ID not found.")
        
@router.delete("/{wallet_id}/delete", tags=["Wallet", "Delete"])
def update_wallet(wallet_id: int, current_user: Annotated[User, Depends(get_current_active_user)]) -> WalletView:
    with get_session() as session:
        wq = (select(Wallet)
                .options(
                    selectinload(Household.users).selectinload(Household.users),
                    selectinload(Household.wallets)
                )
              .where(
                  (Wallet.id == wallet_id) &
                  (Wallet.household.has(
                        Household.users.any(User.id == current_user.id)
                    )
                  )
              )
        )
        result: Wallet = session.execute(wq).scalar_one_or_none()
        if result:
            result.disabled = True
            session.flush()
            return result
        else:
            raise HTTPException(404, "Wallet with given ID not found.")
            
            
            
            
