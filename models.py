from pydantic import BaseModel
from typing import Optional
from typing import Optional, Union

# Request body: Data sent by the client to the server
# Use Pydantic models to define the structure of the request body
class User(BaseModel):
    username: str
    email: str
    disabled: Union[bool, None] 

class UserInDB(User):
    hashed_password: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None]


