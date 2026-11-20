from typing import List, Union

from pydantic import BaseModel
from .summaries import HouseholdSummary

class UserCreate(BaseModel):
    username: str
    password: str
    confirm_password: str
    
class UserDetailsView(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str 
    
class UserDetailsCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str 

class UserDetailsUpdate(BaseModel):
    firstName: str | None
    lastName: str | None
    email: str | None
    phone: str | None

class UserView(BaseModel):
    id: int
    username: str
    details: Union[UserDetailsView, None]
    households: Union[List[HouseholdSummary], None]