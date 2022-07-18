from typing import Optional
from fastapi import Body, FastAPI, Path, Query
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

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required"
        )
):
    return {name: age}
