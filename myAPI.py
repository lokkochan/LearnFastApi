from fastapi import FastAPI, Path, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from dotenv import load_dotenv
import auth
from datetime import timedelta

from models import User, UpdateUser, Token
from Fake_DB import users
from const import TOKEN_EXPIRE_TIME

# Create an instance of FastAPI, this contains attributes and methods to define the API later
app = FastAPI() 

'''
Create an endpoint for the root URL. Endpoint is a function that is called when a client makes a request to the server
For example, amazon.com/delete-user, delete-user is the endpoint, amazon.com is the root URL
That help to specify the service that the client wants to use
'''

# Core HTTP methods: GET (get info), POST (create info), PUT (update info), DELETE (delete info)
@app.get("/") # Decorator that tells FastAPI that this function is an endpoint
def index():    # Function that will be called when the endpoint is accessed
    return users

'''
Endpoint parameters
The parameters are passed in to the function as arguments, some may determine the behavior of the function
Should be dynamic, so that the function can be used for different values
'''

# Path parameters: Parameters that are part of the URL path
# URL example: /users/1, /users/2, /users/3
@app.get("/users/{user_id}") # Define a path parameter by putting it in curly braces
def get_user(user_id: int = Path(description="The ID of user", gt=0, lt=len(users))): # Specify the type of the parameter to be an integer
    # set parameter to None to make it optional
    return users[user_id]

# Query parameters: Parameters that are part of the URL query string
# URL example: /users-by-username?username=johndoe
@app.get("/users-by-username") # Define a query parameter by adding a default value to the function argument
def get_user(username: str):
    for user_id in users:
        if users[user_id]["username"] == username:
            return users[user_id]
    return {"Data": "Not found"}

# Mixed parameters
# URL example: /mix/1?username=johndoe
@app.get("/mix/{user_id}")
def get_user(user_id: int, username: Optional[str] = None): # Optional parameter
    if username:
        if username == users[user_id]["username"]:
            return users[user_id]
        return {"Data": "Not found"}
    return users[user_id]

# POST request
# URL example: /create-user
@app.post("/create-user/{user_id}")
def create_user(user_id: int, user: User):
    if user_id in users:
        return {"Error": "User already exists"}
    users[user_id] = user
    return  users[user_id] 

# PUT request
# URL example: /update-user/1
@app.put("/update-user/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    if user_id not in users:
        return {"Error": "User does not exist"}
    # Update the user information separately to avoid overwriting none on the existing data
    if user.username != None:
        users[user_id]["username"] = user.username
    if user.email != None:
        users[user_id]["email"] = user.email
    return users[user_id]

# DELETE request
# URL example: /delete-user/1
@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        return {"Error": "User does not exist"}
    del users[user_id]
    return {"Message": "User deleted"}


@app.post("/token", response_model=Token) # Token root
async def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends()):
    user= auth.authenticate_user(users, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=TOKEN_EXPIRE_TIME)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/self/", response_model=User)
async def read_users_self(current_user: User = Depends(auth.get_current_active_user)):
    return current_user

@app.get("/users/self/items")
async def read_self_item(current_user: User = Depends(auth.get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}] 

