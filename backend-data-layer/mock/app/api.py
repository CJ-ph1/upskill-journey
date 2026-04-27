from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import services
from .db import get_session, init_db

app = FastAPI(title="backend-data-layer mock")
init_db()


class StudentIn(BaseModel):
    name: str
    email: str
    age: int


class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentIn, db: Session = Depends(get_session)):
    try:
        return services.create_student(
            db, name=payload.name, email=payload.email, age=payload.age,
        )
    except services.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_session)):
    return services.list_students(db)
