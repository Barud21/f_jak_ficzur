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


app.counter = 0
app.patients = []

##############################################################
# Zadanie 1
##############################################################

# @app.get('/')
# def hello_world():
#     return {"message": "Hello World during the coronavirus pandemic!"}


##############################################################
# Zadanie 2
##############################################################

@app.get('/method')
def return_get():
    return {"method": "GET"}

@app.post('/method')
def return_post():
    return {"method": "POST"}

@app.put('/method')
def return_put():
    return {"method": "PUT"}

@app.delete('/method')
def return_delete():
    return {"method": "DELETE"}


##############################################################
# Zadanie 3
##############################################################

class patient_data_rq(BaseModel):
    name: str
    surename: str


class patient_data_resp(BaseModel):
    id: int
    patient: patient_data_rq


@app.post('/patient')
def patient_data(rq: patient_data_rq):
    app.patients.append(rq)
    app.counter += 1
    return patient_data_resp(id=app.counter, patient=rq)


##############################################################
# Zadanie 4
##############################################################

# @app.get('/patient/{pk}')
# def show_patient_data(pk: int):
#     if pk < len(app.patients):
#         return app.patients[pk]
#     else:
#         raise HTTPException(status_code=204, detail="Index not found")


##############################################################
# Zadanie 1
##############################################################

@app.get('/welcome')
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    #return {"message": "Welcome"}
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
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.session_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    response = RedirectResponse("/welcome")
    response.status_code = status.HTTP_302_FOUND
    return response

@app.get("/data")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response.set_cookie(key="session_token", value=session_token)
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

##############################################################
# Zadanie 3
##############################################################

@app.post("/patient")
def add_patient(*, response: Response, patient: patient_data_rq, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if app.counter > len(app.patients):
        app.patients.append(patient)
        app.counter =+ 1
    response.set_cookie(key="session_token", value=session_token)
    response = RedirectResponse(f"/patient/{app.counter-1}")
    response.status_code = status.HTTP_302_FOUND

@app.get("/patient")
def show_patients(response: Response, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return app.patients

@app.get("/patients/{id}")
def show_patient_data(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response.set_cookie(key="session_token", value=session_token)
    if id < len(app.patients):
        return app.patients[id]

@app.delete("patient/{id}")
def delete_patient(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    app.patients.remove(id)
    response.status_code = status.HTTP_204_NO_CONTENT
