from datetime import datetime

from models import mongo_model, clickhouse_model
from models.sql_model import *



def taximetr_mapper_mongo(tax: Taximetr):
    return mongo_model.Taximetr(
        tax.param_id,
        tax.param.name,
        tax.param.units,
        float(tax.param.price),
        float(tax.start_val),
        float(tax.end_val)
    )


def sql_to_mongo_mapper(order: Order):
    taximetr = []
    for tax in order.taximetr:
        taximetr.append(taximetr_mapper_mongo(tax).__dict__)
    return mongo_model.Orders(
        order.id,
        order.client.id,
        order.client.name,
        order.client.ph_num,
        order.client.dc_exist,
        order.client.disc_count,
        order.order_time,
        order.boarding_st_id,
        order.boarding_st.name,
        order.boarding_dist_id,
        order.boarding_dist.name,
        order.boarding_house,
        order.drop_st_id,
        order.drop_st.name,
        order.drop_dist_id,
        order.drop_dist.name,
        order.drop_house,
        order.order_service[0].driver_id,
        order.order_service[0].driver.name,
        order.order_service[0].driver.surname,
        order.order_service[0].driver.p_name,
        datetime.combine(order.order_service[0].driver.birth_date, datetime.min.time()),
        order.order_service[0].driver.work_exp,
        order.order_service[0].driver.ph_num,
        order.order_service[0].driver.car.id,
        order.order_service[0].driver.car.name,
        order.order_service[0].driver.car.color,
        order.order_service[0].driver.car.year,
        datetime.combine(order.order_service[0].start_date, order.order_service[0].start_time),
        datetime.combine(order.order_service[0].end_date, order.order_service[0].end_time),
        taximetr,
        order.status
    )


def click_client_map(client: Client):
    return clickhouse_model.Client(
        id=client.id,
        name=client.name,
        ph_num=client.ph_num,
        dc_exist=client.dc_exist,
        disc_count=client.disc_count
    )


def click_street_map(strt: Street):
    return clickhouse_model.Street(
        id=strt.id,
        name=strt.name
    )


def click_district_map(dist: District):
    return clickhouse_model.District(
        id=dist.id,
        name=dist.name
    )


def click_order_map(order: Order):
    return clickhouse_model.Order(
        id=order.id,
        name=order.name,
        order_time=order.order_time,
        boarding_st_id=order.boarding_st_id,
        boarding_dist_id=order.boarding_dist_id,
        boarding_house=order.boarding_house,
        drop_st_id=order.drop_st_id,
        drop_dist_id=order.drop_dist_id,
        drop_house=order.drop_house,
        status=order.status
    )


def click_car_map(car: Car):
    return clickhouse_model.Car(
        id=car.id,
        name=car.name,
        color=car.color,
        year=car.year
    )


def click_driver_map(dr: Driver):
    return clickhouse_model.Driver(
        id=dr.id,
        surname=dr.surname,
        name=dr.name,
        p_name=dr.p_name,
        birth_date=dr.birth_date,
        work_exp=dr.work_exp,
        car_id=dr.car_id,
        ph_num=dr.ph_num
    )


def click_orderservice_map(os: OrderService):
    return clickhouse_model.Orderservice(
        id=os.id,
        driver_id=os.driver_id,
        start_datetime=datetime.combine(os.start_date, os.start_time),
        end_datetime=datetime.combine(os.end_date, os.end_time),
    )


def click_taximetrtariff_map(tt: TaximetrTariff):
    return clickhouse_model.Taximetrtariff(
        id=tt.id,
        name=tt.name,
        units=tt.units,
        price=tt.price
    )


def click_taximetr_map(tax: Taximetr):
    return clickhouse_model.Taximetr(
        order_id=tax.order_id,
        param_id=tax.param_id,
        start_val=tax.start_val,
        end_val=tax.end_val
    )


# def sql_to_click_mapper():
#     click_client = click_client_map()