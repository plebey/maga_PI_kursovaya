# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import Client


class AccountDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/profile_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id
        self.edit_login.clicked.connect(self.login_edit_click)
        self.edit_pswd.clicked.connect(self.pswd_edit_click)
        self.edit_name.clicked.connect(self.name_edit_click)
        self.edit_ph.clicked.connect(self.ph_edit_click)
        self.edit_card.clicked.connect(self.card_edit_click)

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
        from qt_gui import HistoryClientWindow
        self.hide()
        self.history_client = HistoryClientWindow(self.dbconn, self, self.user_id)
        self.history_client.show()

    def order_btn_click(self):
        from qt_gui import OrderClientWindow
        self.hide()
        self.order_client = OrderClientWindow(self.dbconn, self, self.user_id)
        self.order_client.show()

    def acc_data_insert(self):
        query_result = (
            self.dbconn['sql']
            .query(Client)
            .filter(Client.id == self.user_id)
            .all()
        )
        for client in query_result:
            self.login_e.setText(client.login)
            self.pswd_e.setText(client.pswd)
            self.name_e.setText(client.name)
            self.ph_e.setText(client.ph_num)
            self.card_e.setText(client.card_num)

    def login_edit_click(self):
        if self.login_e.isEnabled():
            text = self.login_e.text()
            client = (
                self.dbconn['sql']
                .query(Client)
                .filter(Client.id == self.user_id)
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
                .query(Client)
                .filter(Client.id == self.user_id)
                .first()
            )
            client.pswd = text
            self.dbconn['sql'].commit()
            self.pswd_e.setEnabled(False)
        else:
            self.pswd_e.setEnabled(True)

    def name_edit_click(self):
        if self.name_e.isEnabled():
            text = self.name_e.text()
            client = (
                self.dbconn['sql']
                .query(Client)
                .filter(Client.id == self.user_id)
                .first()
            )
            client.name = text
            self.dbconn['sql'].commit()
            self.name_e.setEnabled(False)
        else:
            self.name_e.setEnabled(True)

    def ph_edit_click(self):
        if self.ph_e.isEnabled():
            text = self.ph_e.text()
            client = (
                self.dbconn['sql']
                .query(Client)
                .filter(Client.id == self.user_id)
                .first()
            )
            client.ph_num = text
            self.dbconn['sql'].commit()
            self.ph_e.setEnabled(False)
        else:
            self.ph_e.setEnabled(True)

    def card_edit_click(self):
        if self.card_e.isEnabled():
            text = self.card_e.text()
            client = (
                self.dbconn['sql']
                .query(Client)
                .filter(Client.id == self.user_id)
                .first()
            )
            client.card_num = text
            self.dbconn['sql'].commit()
            self.card_e.setEnabled(False)
        else:
            self.card_e.setEnabled(True)
