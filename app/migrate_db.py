from sqlalchemy import create_engine

from db import DATABASE_URL, get_db, session
from models import Base, UsersTable
from auth import pwd_context
from sqlalchemy.orm.session import Session

engine = create_engine(DATABASE_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    user = UsersTable(username="testuser", hashed_password=pwd_context.hash("password"))
    db = session()
    db.add(user)
    db.commit()


if __name__ == "__main__":
    reset_database()
