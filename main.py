from enum import Enum
from typing import Optional
from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

class HairColor(Enum):
    white = "white"
    black = "black"
    brown = "brown"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="First name of the person"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="First name of the person"
        )
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        description="Age of the person"
        )
    hair_color: Optional[HairColor] = Field(default = None)    
    is_maried: Optional[bool] = Field(
        default=False,
        description="Is the person married?"
        )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": 25,
                "hair_color": "brown",
                "is_maried": True
            }
        }

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
        description="This is the person name. It's between 1 and 50 characters",
        example="John Doe"
        ),
    age: int = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required",
        example=25
        )
):
    return {name: age}

@app.get('/person/detail/{person_id}')
def show_person_detail(
    person_id: int = Path(
        ...,
        gt=0,
        lte=100,
        title="Person ID",
        description="This is the person ID. It's between 1 and 100 characters",
        example=123
        ),
):
    return {person_id : "person_id"}

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        lte=100,
        title="Person ID",
        description="This is the person ID. It's between 1 and 100 characters",
        example=123
        ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results