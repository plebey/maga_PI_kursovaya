# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import District, Street


class OrderDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/order_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id
        self.load_dist()
        self.load_from_street()
        self.load_dest_street()
        self.from_dist.currentIndexChanged.connect(self.load_from_street)
        self.to_dist.currentIndexChanged.connect(self.load_dest_street)

        self.account_btn.clicked.connect(self.account_btn_click)
        self.story_btn.clicked.connect(self.history_btn_click)
        # self.radioDriver.toggled.connect(self.driver_selected)
        # self.driver_checked = False
        # self.radioClient.toggled.connect(self.client_selected)
        # self.back.clicked.connect(self.back_to_login)
        # self.client_checked = True
        # self.show()
        # self.client_selected()
        # self.regButton.clicked.connect(self.register_user)

    def account_btn_click(self):
        from qt_gui import AccountClientWindow
        self.hide()
        self.account_client = AccountClientWindow(self.dbconn, self, self.user_id)
        self.account_client.show()

    def history_btn_click(self):
        from qt_gui import HistoryClientWindow
        self.hide()
        self.history_client = HistoryClientWindow(self.dbconn, self, self.user_id)
        self.history_client.show()

    def load_dist(self):
        query_result = (
            self.dbconn['sql']
            .query(District.name)
            .all()
        )
        model = QStandardItemModel()
        # Добавление элементов в модель
        for result in query_result:
            # print(result[0])
            item = QStandardItem(result[0])  # Предполагается, что District.name находится в первом столбце
            model.appendRow(item)
        self.from_dist.setModel(model)
        self.to_dist.setModel(model)

    def load_from_street(self):
        dist = self.from_dist.currentText()
        query_result = (
            self.dbconn['sql']
            .query(District)
            .filter(District.name == dist)
            .all()
        )
        data = []
        model = QStandardItemModel()
        for dist in query_result:
            for street in dist.streets:
                item = QStandardItem(street.name)
                model.appendRow(item)
                data.append(street.name)
        self.from_street.setModel(model)

    def load_dest_street(self):
        dist = self.to_dist.currentText()
        query_result = (
            self.dbconn['sql']
            .query(District)
            .filter(District.name == dist)
            .all()
        )
        data = []
        model = QStandardItemModel()
        for dist in query_result:
            for street in dist.streets:
                item = QStandardItem(street.name)
                model.appendRow(item)
                data.append(street.name)
        self.to_street.setModel(model)



