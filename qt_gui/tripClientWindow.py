from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from models.sql_model import Order


class TripClientWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id, order_id):
        super().__init__()
        loadUi("qt_ui/trip_client.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id
        self.order_id = order_id
        self.set_trip_data()

    def set_trip_data(self):
        order = (
            self.dbconn['sql']
            .query(Order)
            .filter(Order.id == self.order_id)
            .first()
        )
        self.from_dist_l
        self.from_street_l
        self.from_house_l
