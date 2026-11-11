from typing import Union
from decimal import Decimal
from pydantic import BaseModel, Field
from db_models.operations import OperationEnum
from models.summaries import WalletSummary

class OperationCreate(BaseModel):
    name: str
    value: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str
    type: OperationEnum
    wallet_id: int
    
class OperationView(BaseModel):
    name: str
    value: Decimal = Field(max_digits=12, decimal_places=2)
    currency: str
    type: OperationEnum
    wallet: Union[WalletSummary, None]