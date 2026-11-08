from pydantic import BaseModel, ConfigDict


class UserDetailsSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    firstName: str
    lastName: str
    email: str

class UserSummary(BaseModel):
    details: UserDetailsSummary


class HouseholdSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    
class WalletSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    
class OperationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    value: float
    type: str