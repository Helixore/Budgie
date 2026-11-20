from typing import List, Union

from pydantic import BaseModel
from .summaries import UserSummary, WalletSummary

class HouseholdCreate(BaseModel):
    name: str

class HouseholdUpdate(BaseModel):
    name: str | None

class HouseholdView(BaseModel):
    id: int
    name: str
    disabled: bool
    users: Union[List[UserSummary], None]
    wallets: Union[List[WalletSummary], None]
    