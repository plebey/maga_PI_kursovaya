from clickhouse_driver import Client
from pymongo import MongoClient
from sqlalchemy import create_engine, MetaData

from models.clickhouse_model import Base
from utils.conn_str import mssql_conn_str, clickhouse_conn_str
from sqlalchemy.orm import sessionmaker


def sql_connect():
    engine = create_engine(mssql_conn_str)
    metadata = MetaData()
    metadata.bind = engine
    # Создание сессии SQLAlchemy
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, metadata


def mongo_connect():
    client_mongo = MongoClient('mongodb://localhost:27017/')
    return client_mongo


def clickhouse_connect():
    engine_clickhouse = create_engine(clickhouse_conn_str, echo=True)

    Base.metadata.create_all(engine_clickhouse)

    SessionClickHouse = sessionmaker(bind=engine_clickhouse)
    session_clickhouse = SessionClickHouse()
    return session_clickhouse


def clickhouse_connect_for_requests():
    host = 'localhost'  # IP-адрес WSL
    port = 9000  # Порт ClickHouse
    user = 'default'  # Пользователь ClickHouse
    password = ''  # Пароль (если есть)
    database = 'lab4'  # Имя базы данных

    # Создание клиента ClickHouse
    client = Client(host=host, port=port, user=user, password=password, database=database)
    return client