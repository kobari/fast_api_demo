import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


DATABASE = "mysql+pymysql"
ASYNC_DATABASE = "mysql+aiomysql"
USER = "root"
PASSWORD = "mysql"
HOST = "db"
PORT = "3306"
DB_NAME = "db"

DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME
)
ASYNC_DATABASE_URL = "{}://{}:{}@{}:{}/{}".format(
    ASYNC_DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME
)

url = "mysql+pymysql://root:mysql@127.0.0.1/db"

ECHO_LOG = False

engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with session() as session_scope:
        yield session_scope


async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

metadata = sqlalchemy.MetaData()


async def get_async_db():
    async with async_session() as session:
        yield session


Base = declarative_base()
