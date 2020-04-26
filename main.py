from fastapi import FastAPI, HTTPException, Response, Depends, status, Cookie, Request
from fastapi.templating import Jinja2Templates
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
app.secret_key = "secret_KeY so S8cr3T"
security = HTTPBasic()
app.session_tokens = []
templates = Jinja2Templates(directory="templates")

##############################################################
# Zadanie 1
##############################################################

@app.get('/welcome')
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return templates.TemplateResponse("item.html", {"request": request, "user": "trudnY"})

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
    app.session_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    # RedirectResponse(url="/welcome")
    response = RedirectResponse("/welcome")
    response.status_code = status.HTTP_302_FOUND
    return response

@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}
##############################################################
# Zadanie 3
##############################################################

@app.post('/logout')
def logout(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    app.session_tokens.remove(session_token)
    response = RedirectResponse("/")
    return response
