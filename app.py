import json
from contextlib import closing
import fastapi
from fastapi import Response,Depends
from starlette.responses import HTMLResponse
import hashlib 

from db import Session,User
from storage import ExistsError,NotFoundError
from services import store,retrieve,getlist
from exceptions import DbCorruptionError

from jinja2 import Environment,PackageLoader

from fastapi.security import OAuth2PasswordBearer 

app = fastapi.FastAPI()
env = Environment(loader = PackageLoader("templates","."))

# https://fastapi.tiangolo.com/tutorial/security/first-steps/...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/")
def _store(msg: str,token: str = Depends(oauth2_scheme)):
    with closing(Session()) as sess:
        data = msg.encode()
        try:
            written = store(data=data,sess=sess)
        except ExistsError:
            return Response(f"Data exists",status_code=400)
        else:
            return f"stored {msg} @ {written}"

@app.get("/{did}")
def _retrieve(did:str):
    try:
        d = retrieve(did=did).decode()
    except NotFoundError:
        return Response(f"{did} not found", status_code=404)
    except DbCorruptionError as e:
        return Response(str(e), status_code=500)
    else:
        return f"retrieved {d}"

@app.get("/")
def _getlist():
    tpl = env.get_template("list.html")
    env.list_templates()
    gls = getlist()
    return HTMLResponse(tpl.render(ids = gls) )

