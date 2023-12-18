import sys
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy
from sqlalchemy import text


class RegWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow):
        super().__init__()
        loadUi("qt_ui/reg_wind.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow

        self.radioDriver.toggled.connect(self.driver_selected)
        self.driver_checked = False
        self.radioClient.toggled.connect(self.client_selected)
        self.back.clicked.connect(self.back_to_login)
        self.client_checked = True
        self.show()
        self.client_selected()
        self.regButton.clicked.connect(self.register_user)

    def register_user(self):
        if self.driver_checked:
            self.register_driver()
        elif self.client_checked:
            self.register_client()

    def register_driver(self):
        print('driver')

    def register_client(self):
        print('client')

    def driver_selected(self):
        self.driver_checked = True
        self.client_checked = False
        self.fio_l.show()
        self.fio_e.show()
        self.stage_l.show()
        self.stage_e.show()
        self.car_num_l.show()
        self.car_num_e.show()
        self.car_name_l.show()
        self.car_name_e.show()
        self.car_color_l.show()
        self.car_color_e.show()
        self.car_year_l.show()
        self.car_year_e.show()
        self.name_l.hide()
        self.name_e.hide()
        # self.buttom_spacer.changeSize(20, 250, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    def client_selected(self):
        self.client_checked = True
        self.driver_checked = False
        self.name_l.show()
        self.name_e.show()
        self.fio_l.hide()
        self.fio_e.hide()
        self.stage_l.hide()
        self.stage_e.hide()
        self.car_num_l.hide()
        self.car_num_e.hide()
        self.car_name_l.hide()
        self.car_name_e.hide()
        self.car_color_l.hide()
        self.car_color_e.hide()
        self.car_year_l.hide()
        self.car_year_e.hide()
        # self.buttom_spacer.changeSize(20, 250, hData=QSizePolicy.Policy.Maximum)

    def back_to_login(self):
        self.hide()
        self.logWind.show()
