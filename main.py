import random
import sys
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
