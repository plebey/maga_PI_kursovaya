from datetime import datetime

from utils.exec_time import exec_time_wrapper


@exec_time_wrapper
def nissan_orders(collection):
    # Запрос на получение заявок на машине Nissan
    nissan_requests = collection.find({"car_brand": "Nissan"})
    # print(nissan_requests)
    # Вывод данных
    # for req in nissan_requests:
    #     print(f"Mongo: Заявка {req} выполнена на машине марки 'nissan'")


@exec_time_wrapper
def orders_2022(collection):
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    end_date = datetime(2022, 12, 31, 23, 59, 59)

    query = {'req_time': {'$gte': start_date, '$lte': end_date}}
    req_lst = collection.count_documents(query)
    print(f"Mongo: Заявок {req_lst} выполнено в 2022 году")


@exec_time_wrapper
def count_orders_with_disc(collection):

    pipeline = [
        {
            "$match": {
                "cl_card": True  # Фильтрация по наличию дисконтной карты
            }
        },
        {
            "$group": {
                "_id": None,
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "count": 1
            }
        }
    ]
    result = list(collection.aggregate(pipeline))

    # Вывод результата
    if result:
        print(f"Mongo: Количество заявок с дисконтной картой: {result[0]['count']}")
    else:
        print("Нет заявок с дисконтной картой.")


