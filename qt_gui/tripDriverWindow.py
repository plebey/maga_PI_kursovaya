from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi


class TripDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/trip_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id