from typing import Union

from pydantic import BaseModel
from db_models.operations import OperationEnum
from models.summaries import WalletSummary

class OperationCreate(BaseModel):
    name: str
    value: float
    type: OperationEnum
    wallet_id: int
    
class OperationView(BaseModel):
    name: str
    value: float
    type: OperationEnum
    wallet: Union[WalletSummary, None]