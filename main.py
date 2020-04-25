from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
app.counter = 0
app.patients = []

##############################################################
# Zadanie 1
##############################################################

@app.get('/welcome')
def welcome():
    return {"message": "Welcome"}

@app.get('/')
def hello():
    return {"message": "Hello World!"}

##############################################################
# Zadanie 2
##############################################################
