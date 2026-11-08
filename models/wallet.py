from typing import List, Union

from pydantic import BaseModel

from .summaries import OperationSummary, HouseholdSummary

class WalletCreate(BaseModel):
    household_id: int
    name: str
    
class WalletView(BaseModel):
    id: int
    name: str
    operations: List[Union[OperationSummary, None]]
    household: Union[HouseholdSummary, None]