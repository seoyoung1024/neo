from fastapi import FastAPI
from pydantic import BaseModel
from database import db_conn
from models import St_info, St_grade

app = FastAPI()

db = db_conn()
session = db.sessionmaker()

class Item(BaseModel):
    name: str
    number : int

@app.get('/')
async def HealthCheck():
    print("{'message' : 'OK'}")
    return {"message": "OK"}

@app.get('/st_info')
async def Select_st_info():
    result = session.query(St_info)
    print(result.all())
    return result.all()

@app.get('/st_grade')
async def Select_st_info():
    result = session.query(St_grade)
    return result.all()

@app.get('/getuser')
async def getuser(id=None, name=None):
    if (id is None)and (name is None):
        return "id, name을 입력"
    else:
        if id is None:
            return session.query(User).filter_by(name=name).all()
        elif name is None:
            return session.query(User).filter_by(id=id).all()
        else:
            return session.query(User).filter_by(id=id).filter_by(name=name).all()

@app.get('/useradd')
async def getuser(id=None, name=None):
    if (id is None) or (name is None) or (dept is None):
        return "id, name, dept를 입력"
    else:
        user = St_info(ST_ID=id, NAME=name, DEPT=dept)
        session.add(user)
        session.commit()
        result = session.query(St_info).all()
        return result

@app.get('/userupdate')
async def getuser(id=None, name=None):
    if (id is None) or (name is None) or (dept is None):
        return "id, name, dept를 입력"
    else:
        user = session.query(St_info).filter(St_info.ST_ID == id).first()
        user.NAME = name
        user.DEPT = dept
        session.add(user)
        session.commit()
        result = session.query(St_info).filter(St_info.ST_ID == id).allfirst()
        return result
