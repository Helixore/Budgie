from typing import List, Union

from pydantic import BaseModel
from .summaries import UserSummary, WalletSummary

class HouseholdCreate(BaseModel):
    name: str

class HouseholdView(BaseModel):
    name: str
    users: Union[List[UserSummary], None]
    wallets: Union[List[WalletSummary], None]
    