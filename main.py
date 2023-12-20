# -*- coding: utf-8 -*-
import random
import sys

from sqlalchemy import select, text, desc
from sqlalchemy.orm import aliased

from models import sql_model
from models.sql_model import OrderService, Car, Client, Order, Street, District, Taximetr, Driver
from utils.db_connect import sql_connect, mongo_connect, clickhouse_connect
from modules.export_db import export_mssql_to_clickhouse, export_mssql_to_mongo
from modules.exec_requests import sql_requests, clickhouse_requests, mongo_requests
# from modules import TaxiApp
from qt_gui import LoginWindow
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    # Подключение к MS SQL
    session_sql, metadata = sql_connect()
    engine = session_sql.get_bind()

    # Подключение к MongoDB
    client_mongo = mongo_connect()
    db_mongo = client_mongo['lab3']
    collection_mongo = db_mongo['main']

    dbconn = {
        'sql': session_sql,
        'mongo': collection_mongo
    }

    # username_to_query = 'client'
    # users_with_desired_username = dbconn['sql'].query(sql_model.Client).filter(sql_model.Client.login == username_to_query).all()
    # print(users_with_desired_username)
    # for user in users_with_desired_username:
    #     print(f"User ID: {user.id}, Username: {user.login}, Email: {user.name}")

    # last_id = dbconn['sql'].query(sql_model.Client).order_by(desc(sql_model.Client.id)).first().id
    # new_client = sql_model.Client(
    #     id=last_id+1,
    #     login='login',
    #     pswd='login',
    #     name='login',
    #     ph_num='login',
    # )
    # # Добавьте нового клиента в сессию
    # dbconn['sql'].add(new_client)
    # # Закоммитить изменения в базе данных
    # dbconn['sql'].commit()

    # query_result = (
    #     dbconn['sql']
    #     .query(Client)
    #     .filter(Client.id == 1)
    #     .all()
    # )
    # orders = []
    # for elem in query_result:
    #     for i, order in enumerate(elem.orders):
    #         for service in order.order_service:
    #             price = 0
    #             for tax in service.taximetr:
    #                 price = price + (tax.value * tax.param.price)
    #
    #         orders.append({order.id: {
    #             'time': order.order_time,
    #             'board_street': order.boarding_st.name,
    #             'board_dist': order.boarding_dist.name,
    #             'board_house': order.boarding_house,
    #             'drop_street': order.drop_st.name,
    #             'drop_dist': order.drop_dist.name,
    #             'drop_house': order.drop_house,
    #             'status': order.status,
    #             'driver': order.order_service[0].driver.name,
    #             'car_num': order.order_service[0].driver.car_id,
    #             'cost': price,
    #         }})
    # orders_str = []
    # for i, ord in enumerate(orders):
    #     # for order in ord:
    #     for order in ord.values():
    #         print(order)
    #         orders_str.append(
    #             f'''
    #                     Заявка №{i + 1}:
    #                     Время заявки: {order['time'].strftime("%Y-%m-%d %H:%M:%S")}
    #                     Место посадки: {order['board_dist']} {order['board_street']} {order['board_house']}
    #                     Место высадки: {order['drop_dist']} {order['drop_street']} {order['drop_house']}
    #                     Водитель: {order['driver']}
    #                     Номер авто: {order['car_num']}
    #                     Сумма: {order['cost']}
    #                     Статус: {order['status']}
    #                     '''
    #         )


    # query_result = (
    #     dbconn['sql']
    #     .query(Client)
    #     .filter(Client.id == 1)
    #     .all()
    # )
    # orders = []
    # for elem in query_result:
    #     for i, order in enumerate(elem.orders):
    #         for service in order.order_service:
    #             price = 0
    #             for tax in service.taximetr:
    #                 price = price + (tax.value * tax.param.price)
    #
    #         orders.append({order.id: {
    #             'time': order.order_time,
    #             'board_street': order.boarding_st.name,
    #             'board_dist': order.boarding_dist.name,
    #             'board_house': order.boarding_house,
    #             'drop_street': order.drop_st.name,
    #             'drop_dist': order.drop_dist.name,
    #             'drop_house': order.drop_house,
    #             'status': order.status,
    #             'driver': order.order_service[0].driver.name,
    #             'car_num': order.order_service[0].driver.car_id,
    #             'cost': price,
    #         }})



    app = QApplication(sys.argv)

    window = LoginWindow(dbconn)
    sys.exit(app.exec())



    # Подключение к Clickhouse
    # session_clk = clickhouse_connect()

    # Генерация данных
    # data = {
        # 'client': session.query(sql_model.Client).all(),
        # 'street': session.query(sql_model.Street).all(),
        # 'district': session.query(sql_model.District).all(),
        # # 'st_dist': session.query(sql_model.StreetsDistricts).all(),
        # 'order': session.query(sql_model.Order).all(),
        # 'car': session.query(sql_model.Car).all(),
        # 'driver': session.query(sql_model.Driver).all(),
        # 'orderservice': session.query(sql_model.OrderService).all(),
        # 'taximetrtariff': session.query(sql_model.TaximetrTariff).all(),
        # 'taximetr': session.query(sql_model.Taximetr).all()
    # }

    # insert_data.insert_into_mssql(session, data)

    # Перенос из mssql в mongodb
    # export_mssql_to_mongo(session, collection_mongo)

    # Перенос из mssql в clickhouse
    # export_mssql_to_clickhouse(session, session_clk, data)

    # Запросы
    # print('SQL: ')
    # sql_requests(session)
    # # print('Mongo: ')
    # # mongo_requests(collection_mongo)
    # print('Clickhouse: ')
    # clickhouse_requests()

    # client_clk.disconnect()
    # session.close()
    # client_mongo.close()
