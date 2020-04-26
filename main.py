from fastapi import FastAPI, HTTPException, Response, Depends, status, Cookie
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
app.secret_key = "secret_KeY so S8cr3T"
security = HTTPBasic()
session_tokens = []

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

@app.post('/login')
def get_current_username(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}")).hexdigest
    response.set_cookie(key="session_token", value=session_token)
    # RedirectResponse(url="/welcome")
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND

@app.get("/data")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in session_tokens:
        raise HTTPException(status_code=403, detail="Unauthorised")
    response.set_cookie(key="session_token", value=session_token)

##############################################################
# Zadanie 3
##############################################################

@app.post('/logout')
def logout(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorised")
    session_tokens.remove(session_token)
    return RedirectResponse("/")