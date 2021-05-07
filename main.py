from fastapi import FastAPI,Depends,status
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager #Loginmanager Class
from fastapi.templating import Jinja2Templates
from fastapi_login.exceptions import InvalidCredentialsException #Exception class
import path

app= FastAPI()
# openssl rand -hex 32
SECRET = "22911e69619b6a7c44599493a6cb983594976d6ff3bba06bff8f7e22f6affb95"

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, tokenUrl="/auth/login", use_cookie=True)
manager.cookie_name = "some-name"

DB = {"username":{"password":"secret-password"}} # unhashed

@manager.user_loader
def load_user(username:str):
    user = DB.get(username)
    return user

@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub":username}
    )
    resp = RedirectResponse(url="/private",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp

@app.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"

@app.get("/",response_class=HTMLResponse)
def loginwithCreds(request:Request):
    with open(path.join(pth, "templates/login.html")) as f:
        return HTMLResponse(content=f.read())