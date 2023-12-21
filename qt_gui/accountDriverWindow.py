# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import Client, Driver


class AccountDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/profile_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id
        self.edit_login.clicked.connect(self.login_edit_click)
        self.edit_pswd.clicked.connect(self.pswd_edit_click)
        self.edit_ph.clicked.connect(self.ph_edit_click)

        self.acc_data_insert()
        self.story_btn.clicked.connect(self.history_btn_click)
        self.taxi_btn.clicked.connect(self.order_btn_click)
        # self.radioDriver.toggled.connect(self.driver_selected)
        # self.driver_checked = False
        # self.radioClient.toggled.connect(self.client_selected)
        # self.back.clicked.connect(self.back_to_login)
        # self.client_checked = True
        # self.show()
        # self.client_selected()
        # self.regButton.clicked.connect(self.register_user)

    def history_btn_click(self):
        from qt_gui import HistoryDriverWindow
        self.hide()
        self.history_driver = HistoryDriverWindow(self.dbconn, self, self.user_id)
        self.history_driver.show()

    def order_btn_click(self):
        from qt_gui import OrderDriverWindow
        self.hide()
        self.order_driver = OrderDriverWindow(self.dbconn, self, self.user_id)
        self.order_driver.show()

    def acc_data_insert(self):
        query_result = (
            self.dbconn['sql']
            .query(Driver)
            .filter(Driver.id == self.user_id)
            .all()
        )
        for driver in query_result:
            self.login_e.setText(driver.login)
            self.pswd_e.setText(driver.pswd)
            self.surname_e.setText(driver.surname)
            self.name_e.setText(driver.name)
            self.pname_e.setText(driver.p_name)
            self.surname_e.setText(driver.surname)
            self.bday_e.setText(driver.birth_date.strftime("%Y-%m-%d"))
            self.ph_e.setText(driver.ph_num)
            self.car_num_e.setText(driver.car_id)
            self.car_name_e.setText(driver.car.name)

    def login_edit_click(self):
        if self.login_e.isEnabled():
            text = self.login_e.text()
            client = (
                self.dbconn['sql']
                .query(Driver)
                .filter(Driver.id == self.user_id)
                .first()
            )
            client.login = text
            self.dbconn['sql'].commit()
            self.login_e.setEnabled(False)
        else:
            self.login_e.setEnabled(True)

    def pswd_edit_click(self):
        if self.pswd_e.isEnabled():
            text = self.pswd_e.text()
            client = (
                self.dbconn['sql']
                .query(Driver)
                .filter(Driver.id == self.user_id)
                .first()
            )
            client.pswd = text
            self.dbconn['sql'].commit()
            self.pswd_e.setEnabled(False)
        else:
            self.pswd_e.setEnabled(True)

    def ph_edit_click(self):
        if self.ph_e.isEnabled():
            text = self.ph_e.text()
            client = (
                self.dbconn['sql']
                .query(Driver)
                .filter(Driver.id == self.user_id)
                .first()
            )
            client.ph_num = text
            self.dbconn['sql'].commit()
            self.ph_e.setEnabled(False)
        else:
            self.ph_e.setEnabled(True)

    def closeEvent(self, event):
        driver = (
            self.dbconn['sql']
            .query(Driver)
            .filter(Driver.id == self.user_id)
            .first()
        )
        driver.status = 'Неактивен'
        self.dbconn['sql'].commit()
        event.accept()

