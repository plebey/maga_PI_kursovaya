import random
from datetime import datetime, timedelta

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from models import sql_model


def insert_into_orders(session: Session, count, clients, streets, dists):
    last_ord_id = session.query(sql_model.Order).order_by(desc(sql_model.Order.id)).first().id
    start_datetime = datetime(2023, 1, 1, 0, 0, 0)
    end_datetime = datetime(2023, 1, 1, 23, 59, 59)
    time_delta = end_datetime - start_datetime
    data = []
    for i in range(count):
        random_seconds = random.randint(0, int(time_delta.total_seconds()))
        random_datetime = start_datetime + timedelta(seconds=random_seconds)
        last_ord_id = last_ord_id + 1
        row = {
            'Код': last_ord_id,
            'КодКлиента': random.choice(clients).id,
            'ВремяЗаявки': random_datetime,
            'УлицаПосадки': random.choice(streets).id,
            'РайонПосадки': random.choice(dists).id,
            'ДомПосадки': random.randint(1, 150),
            'УлицаОкПосадки': random.choice(streets).id,
            'РайонОкПосадки': random.choice(dists).id,
            'ДомОкПосадки': random.randint(1, 150),
            'Статус': random.choice(['Успешно', 'Проблема'])
        }
        print(f'ord: {row}')
        data.append(row)

    session.execute(sql_model.Order.__table__.insert(), data)
    # Подтвердите транзакцию
    session.commit()


def insert_into_orderservice(session: Session, count, driver):
    last_ordserv_id = session.query(sql_model.OrderService).order_by(desc(sql_model.OrderService.id)).first().id
    start_datetime = datetime(2023, 1, 1, 0, 0, 0)
    end_datetime = datetime(2023, 1, 1, 23, 59, 59)
    time_delta = end_datetime - start_datetime

    data = []
    for i in range(count):
        random_seconds = random.randint(0, int(time_delta.total_seconds()))
        random_datetime_start = start_datetime + timedelta(seconds=random_seconds)

        random_seconds = random.randint(0, int(10000))
        random_datetime_end = random_datetime_start + timedelta(seconds=random_seconds)

        last_ordserv_id = last_ordserv_id + 1
        row = {
            'Код': last_ordserv_id,
            'Водитель': random.choice(driver).id,
            'ДатаНач': random_datetime_start,
            'ВремяНач': random_datetime_start,
            'ДатаОк': random_datetime_end + timedelta(seconds=random_seconds),
            'ВремяОк': random_datetime_end + timedelta(seconds=random_seconds),
            }
        print(f'ordserv: {row}')
        data.append(row)

    session.execute(sql_model.OrderService.__table__.insert(), data)
    # Подтвердите транзакцию
    session.commit()


def insert_into_tax(session: Session, count):
    last_ord_id = session.query(sql_model.Taximetr).order_by(desc(sql_model.Taximetr.order_id)).first().order_id
    data = []
    for i in range(count):
        start = random.uniform(0, 100)
        last_ord_id = last_ord_id + 1
        row = {
            'КодЗаявки': last_ord_id,
            'КодПараметра': 1,
            'НачЗнач': start,
            'КонЗнач': random.uniform(start, 100),
        }
        print(f'tax_1: {row}')
        data.append(row)

        row = {
            'КодЗаявки': last_ord_id,
            'КодПараметра': 2,
            'НачЗнач': start,
            'КонЗнач': random.uniform(start, 100),
        }
        print(f'tax_2: {row}')
        data.append(row)

        row = {
            'КодЗаявки': last_ord_id,
            'КодПараметра': 3,
            'НачЗнач': start,
            'КонЗнач': random.uniform(start, 100),
        }
        print(f'tax_3: {row}')
        data.append(row)

    session.execute(sql_model.Taximetr.__table__.insert(), data)
    # Подтвердите транзакцию
    session.commit()


def insert_into_mssql(session: Session, data):
    count = 200000
    insert_into_orders(session, count, data['clients'], data['streets'], data['districts'])
    insert_into_orderservice(session, count, data['drivers'])
    insert_into_tax(session, count)
