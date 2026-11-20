from typing import List, Union

from pydantic import BaseModel

from .summaries import OperationSummary, HouseholdSummary

class WalletCreate(BaseModel):
    household_id: int
    name: str
    
class WalletUpdate(BaseModel):
    name: str | None

class WalletView(BaseModel):
    id: int
    name: str
    disabled: bool
    operations: Union[List[OperationSummary], None]
    household: Union[HouseholdSummary, None]