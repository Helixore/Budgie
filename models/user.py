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

class UserView(BaseModel):
    username: str
    details: Union[UserDetailsView, None]
    households: Union[List[HouseholdSummary], None]