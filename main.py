from email.policy import default
from enum import Enum
from typing import Optional
from fastapi import Body, Cookie, FastAPI, Form, Header, Path, Query, status
from pydantic import BaseModel, EmailStr, Field

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

class BasePerson(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="First name of the person",
        example="John",
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="First name of the person",
        example="Doe"
        )
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        description="Age of the person",
        example=25
        )
    email: EmailStr = Field(
        ...,
        description="Email of the person",
        example="asd@asd.com"
        )
    hair_color: Optional[HairColor] = Field(default = None)    
    is_maried: Optional[bool] = Field(
        default=False,
        description="Is the person married?",
        example=False
        )

class Person(BasePerson): 
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Password of the person",
        example='12345678'
        )

class PersonOut(BaseModel):
    pass

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="User name of the person",
        example="John@20"
        )
    message: str = Field(
        default="Login successful",
        description="Message of the login",
        example="Login successful"
        )

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post('/person', status_code=status.HTTP_201_CREATED, response_model=BasePerson)
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
    person: BasePerson = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results

@app.post('/login', response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), pasword: str = Form(...)):
    return LoginOut(username=username)

@app.post('/contact', status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(
        ...,
        min_length=1,
        max_length=20
        ),
    last_name: str = Form(
        ...,
        min_length=1,
        max_length=20
        ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
        ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),   
):
    return user_agent