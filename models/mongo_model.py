from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Any, List


@dataclass
class Taximetr:
    code: int
    name: str
    units: str
    price: float
    init_val: float
    final_val: float


@dataclass
class Orders:
    ord_id: int
    cl_code: int
    cl_name: str
    cl_ph_num: str
    cl_card: bool
    cl_percent_count: int
    req_time: datetime
    land_str_id: int
    land_str_name: str
    land_area_id: int
    land_area_name: str
    land_house: str
    end_str_id: int
    end_str_name: str
    end_area_id: int
    end_area_name: str
    end_house: str
    driver_id: int
    dr_name: str
    dr_surname: str
    dr_pname: str
    dr_birth: datetime
    dr_expir: int
    dr_ph_num: str
    car_num: int
    car_brand: str
    car_color: str
    car_year: int
    start_date: datetime
    end_date: datetime
    taximetr: List['Taximetr']
    status: str
