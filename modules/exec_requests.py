from modules import mssql_req, mongo_req, insert_data, clickhouse_req
from utils.db_connect import clickhouse_connect_for_requests


def sql_requests(session):
    mssql_req.nissan_orders(session)
    # mssql_req.orders_2022(session)
    # mssql_req.count_orders_with_disc(session)


def mongo_requests(collection_mongo):
    mongo_req.nissan_orders(collection_mongo)
    mongo_req.orders_2022(collection_mongo)
    mongo_req.count_orders_with_disc(collection_mongo)


def clickhouse_requests():
    clk_client = clickhouse_connect_for_requests()
    clickhouse_req.nissan_orders(clk_client)
    # clickhouse_req.orders_2022(clk_client)
    # clickhouse_req.count_orders_with_disc(clk_client)
    clk_client.disconnect()