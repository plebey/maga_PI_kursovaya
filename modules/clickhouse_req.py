from utils.exec_time import exec_time_wrapper
from clickhouse_driver import Client


# TODO: добавить госномер в индекс
@exec_time_wrapper
def nissan_orders(client: Client):
    req = """\
        SELECT order_time, status \
        FROM order \
        JOIN orderservice ON order.id = orderservice.id \
        JOIN driver ON orderservice.driver_id = driver.id \
        JOIN car ON driver.car_id = car.id \
        WHERE car.name = 'Nissan'
    """
    req_nissan = client.execute(req)
    # Вывод результатов
    # for req in req_nissan:
    #     print(f"Sql: Заявка {req} выполнена на машине марки 'nissan'")


# TODO: Добавить время в индекс
@exec_time_wrapper
def orders_2022(client: Client):

    req_txt = '''
    SELECT COUNT(*)  \
    FROM order  \
    WHERE order_time BETWEEN '2022-01-01T00:00:00' AND '2022-12-31T23:59:59';
    '''
    req_lst = client.execute(req_txt)
    # Получение результата
    result = req_lst

    # Вывод результата
    if result:
        count = result[0][0]
        print(f"Clickhouse:\nКоличество заявок выполненных в 2022 году: {count}")
    else:
        print("Результат не найден")


# TODO: Добавить наличиедиск карты в индекс
@exec_time_wrapper
def count_orders_with_disc(client: Client):

    req_txt = '''
        SELECT COUNT(*)  \
        FROM order  \
        INNER JOIN client ON order.name = client.id  \
        WHERE client.dc_exist = 1;
        '''
    req_lst = client.execute(req_txt)

    # Получение результата
    result = req_lst

    # Вывод результата
    if result:
        count = result[0][0]
        print(f"Clickhouse:\nКоличество заявок от клиентов с картой: {count}")
    else:
        print("Результат не найден")
