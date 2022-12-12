from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm.session import Session

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from db import get_db, AsyncSession, get_async_db
from models import (
    PersonsTable,
    InterviewsTable,
)
from auth import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from schema import (
    User,
    PersonCreateResponse,
    PersonCreate,
    InterviewCreate,
    InterviewCreateResponse,
    Registration,
    RegistrationResponse,
)

app = FastAPI()
router = APIRouter()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/person", response_model=PersonCreateResponse)
async def create_person(body: PersonCreate, db: Session = Depends(get_db)):
    person = PersonsTable(**body.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.get("/person")
async def list_person(db: AsyncSession = Depends(get_async_db)):
    result: Result = await db.execute(select(PersonsTable))
    return result.all()


@router.post("/interview", response_model=InterviewCreateResponse)
async def create_interview(body: InterviewCreate, db: Session = Depends(get_db)):
    interview = InterviewsTable(**body.dict())
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return interview


@router.get("/interview")
async def list_interview(db: AsyncSession = Depends(get_async_db)):
    result: Result = await db.execute(select(InterviewsTable))
    return result.all()


@router.post("/registration", response_model=RegistrationResponse)
async def create_registration(
    body: Registration,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    問診票と患者の登録を行います
    患者のデータはなくても登録が行えます
    Args:
        body: 問診票と患者の登録データ
        current_user: ログインユーザを取得
        db: DB接続インスタンスを取得
    """
    try:
        person = None
        if body.person:
            person = PersonsTable(**body.person.dict())
            db.add(person)
            db.flush()
            db.refresh(person)

        interview = InterviewsTable(**body.interview.dict())
        if person:
            interview.person_id = person.id
        db.add(interview)
        db.commit()
        db.refresh(interview)
        return {"person": person, "interview": interview}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration Error")


app.include_router(router)
