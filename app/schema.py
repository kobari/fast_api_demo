from pydantic import BaseModel, Field, validator
from datetime import datetime


class Person(BaseModel):
    name: str
    sex: str = Field("man")
    weight: float
    height: float
    age: int

    @validator("sex")
    def validate_sex(cls, value):
        if value not in ["man", "woman"]:
            raise TypeError(f"{value} is an allowed value")
        return value


class PersonCreate(Person):
    pass


class PersonCreateResponse(Person):
    id: int

    class Config:
        orm_mode = True


class Interview(BaseModel):
    when: datetime
    how: str
    question1: str | None = None
    question2: str | None = None
    person_id: int | None = None


class InterviewCreate(Interview):
    pass


class InterviewCreateResponse(Interview):
    id: int

    class Config:
        orm_mode = True


class Registration(BaseModel):
    person: PersonCreate | None = None
    interview: InterviewCreate = None


class RegistrationResponse(BaseModel):
    """ユーザ登録と診断結果を登録"""

    person: PersonCreateResponse | None = None
    interview: InterviewCreateResponse = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
