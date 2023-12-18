from sqlalchemy import create_engine, Column, MetaData, literal
from clickhouse_sqlalchemy import (
    Table, make_session, get_declarative_base, types, engines
)


Base = get_declarative_base()


class Client(Base):
    id = Column(types.Int32, primary_key=True)
    name = Column(types.String)
    ph_num = Column(types.String)
    dc_exist = Column(types.Boolean)
    disc_count = Column(types.Decimal(precision=10, scale=2))
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Street(Base):
    id = Column(types.Int32, primary_key=True)
    name = Column(types.String)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class District(Base):
    id = Column(types.Int32, primary_key=True)
    name = Column(types.String)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Order(Base):
    id = Column(types.Int32, primary_key=True, autoincrement=False)
    name = Column(types.Int32)
    order_time = Column(types.DateTime)
    boarding_st_id = Column(types.Int32)
    boarding_dist_id = Column(types.Int32)
    boarding_house = Column(types.String)
    drop_st_id = Column(types.Int32)
    drop_dist_id = Column(types.Int32)
    drop_house = Column(types.String)
    status = Column(types.String)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Car(Base):
    id = Column(types.String, primary_key=True)
    name = Column(types.String)
    color = Column(types.String)
    year = Column(types.Int32)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Driver(Base):

    id = Column(types.Int32, primary_key=True)
    surname = Column(types.String)
    name = Column(types.String)
    p_name = Column(types.String)
    birth_date = Column(types.Date)
    work_exp = Column(types.Int32)
    car_id = Column(types.String)
    ph_num = Column(types.String)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Orderservice(Base):
    id = Column(types.Int32, primary_key=True)
    driver_id = Column(types.Int32)
    start_datetime = Column(types.DateTime)
    end_datetime = Column(types.DateTime)
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Taximetrtariff(Base):
    id = Column(types.Int32, primary_key=True)
    name = Column(types.String)
    units = Column(types.String)
    price = Column(types.Decimal(precision=10, scale=2))
    __table_args__ = (
        engines.MergeTree(order_by='id'),
    )


class Taximetr(Base):
    order_id = Column(types.Int32, primary_key=True)
    param_id = Column(types.Int32, primary_key=True)
    start_val = Column(types.Decimal(precision=10, scale=2))
    end_val = Column(types.Decimal(precision=10, scale=2))
    __table_args__ = (
        engines.MergeTree(order_by=('order_id', 'param_id')),
    )




