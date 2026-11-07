from typing import Union

from pydantic import BaseModel

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