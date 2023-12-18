from modules import mapper
from models import sql_model, clickhouse_model


def export_mssql_to_clickhouse(session, session_clk, data:dict=None):
    for key in data.keys():
        class_name = key.capitalize()
        attributes = []
        data[key] = data[key][420677:]
        for obj in data[key]:
            function_name = "click_" + key + "_map"
            # mapped_obj = getattr(__name__, function_name)(obj)

            click_function = globals()[function_name]
            mapped_obj = click_function(obj)

            attributes.append(mapped_obj.__dict__)
            attributes[-1].pop('_sa_instance_state', None)
            print(attributes[-1])

        module_name = 'models.clickhouse_model'
        module = __import__(module_name, fromlist=[class_name])
        _class = getattr(module, class_name)

        session_clk.execute(_class.__table__.insert().values(attributes))


def export_mssql_to_mongo(session, collection_mongo):
    orders = session.query(sql_model.Order).all()

    for order in orders:
        order_mongo = mapper.sql_to_mongo_mapper(order)
        print(order_mongo.__dict__)
        collection_mongo.insert_one(order_mongo.__dict__)