from sqlalchemy import text
from utils.exec_time import exec_time_wrapper

# TODO: добавить госномер в индекс
@exec_time_wrapper
def nissan_orders(session):

    req = text("""
    SELECT Заявки.ВремяЗаявки, Заявки.Статус
    FROM Заявки
    JOIN ОбслуживаниеЗаявок ON Заявки.Код = ОбслуживаниеЗаявок.Код
    JOIN Водители ON ОбслуживаниеЗаявок.Водитель = Водители.Код
    JOIN Машины ON Водители.ГосНомер = Машины.ГосНомер
    WHERE Машины.Марка = 'nissan'
""")
    req_nissan = session.execute(req)
    # Вывод результатов
    # for req in req_nissan:
    #     print(f"Sql: Заявка {req} выполнена на машине марки 'nissan'")


# TODO: Добавить время в индекс
@exec_time_wrapper
def orders_2022(session):

    req_txt = text('''
    SELECT COUNT(*) 
    FROM Заявки 
    WHERE ВремяЗаявки BETWEEN '2022-01-01T00:00:00' AND '2022-12-31T23:59:59';
    ''')
    req_lst = session.execute(req_txt)

    # Получение результата
    result = req_lst.fetchone()

    # Вывод результата
    if result:
        count = result[0]
        print(f"Sql: Количество заявок выполненных в 2022 году: {count}")
    else:
        print("Результат не найден")


# TODO: Добавить наличиедиск карты в индекс
@exec_time_wrapper
def count_orders_with_disc(session):
    req_txt = text('''
        SELECT COUNT(*) 
        FROM Заявки 
        INNER JOIN Клиенты ON Заявки.КодКлиента = Клиенты.Код 
        WHERE Клиенты.НаличиеДисконтКарты = 1;
        ''')
    req_lst = session.execute(req_txt)

    # Получение результата
    result = req_lst.fetchone()

    # Вывод результата
    if result:
        count = result[0]
        print(f"Sql: Количество заявок от клиентов с картой: {count}")
    else:
        print("Результат не найден")
