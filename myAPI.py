from fastapi import FastAPI

# Create an instance of FastAPI, this contains attributes and methods to define the API later
app = FastAPI() 

# Create an endpoint for the root URL. Endpoint is a function that is called when a client makes a request to the server
# For example, amazon.com/delete-user, delete-user is the endpoint, amazon.com is the root URL
# That help to specify the service that the client wants to use

# Core HTTP methods: GET (get info), POST (create info), PUT (update info), DELETE (delete info)
@app.get("/") # Decorator that tells FastAPI that this function is an endpoint
def index():    # Function that will be called when the endpoint is accessed
    return {"message": "Hello, World"}