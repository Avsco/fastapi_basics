from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_maried: Optional[bool] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/person')
def create_person(person: Person = Body(...)):
    return person.dict()