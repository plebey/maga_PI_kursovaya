# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt, QAbstractListModel, QVariant
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import Client, Car, Order, OrderService, Street, District, Taximetr, Driver


class MyListModel(QAbstractListModel):
    def __init__(self, data=[], parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()])
        return QVariant()


class HistoryDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/order_history_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id

        self.account_btn.clicked.connect(self.account_btn_click)
        self.taxi_btn.clicked.connect(self.order_btn_click)
        self.update_list_view()
        # self.radioDriver.toggled.connect(self.driver_selected)
        # self.driver_checked = False
        # self.radioClient.toggled.connect(self.client_selected)
        # self.back.clicked.connect(self.back_to_login)
        # self.client_checked = True
        # self.show()
        # self.client_selected()
        # self.regButton.clicked.connect(self.register_user)

    def account_btn_click(self):
        from qt_gui import AccountDriverWindow
        self.hide()
        self.account_driver = AccountDriverWindow(self.dbconn, self, self.user_id)
        self.account_driver.show()

    def order_btn_click(self):
        from qt_gui import OrderDriverWindow
        self.hide()
        self.order_driver = OrderDriverWindow(self.dbconn, self, self.user_id)
        self.order_driver.show()

    def update_list_view(self):
        query_result = (
            self.dbconn['sql']
            .query(Driver)
            .filter(Driver.id == self.user_id)
            .all()
        )
        orders = []

        for driver in query_result:
            for i, ord_serv in enumerate(driver.order_service):
                cost = 0
                for tax in ord_serv.taximetr:
                    cost = cost + (tax.value * tax.param.price)
                cost = float(cost) * 0.9

                orders.append({ord_serv.order.id: {
                    'time': ord_serv.order.order_time,
                    'board_street': ord_serv.order.boarding_st.name,
                    'board_dist': ord_serv.order.boarding_dist.name,
                    'board_house': ord_serv.order.boarding_house,
                    'drop_street': ord_serv.order.drop_st.name,
                    'drop_dist': ord_serv.order.drop_dist.name,
                    'drop_house': ord_serv.order.drop_house,
                    'status': ord_serv.order.status,
                    'client': ord_serv.order.client.ph_num,
                    'cl_name': ord_serv.order.client.name,
                    'cost': cost,
                }}
                )
        orders_str = []
        for i, ord in enumerate(orders):
            # for order in ord:
            for order in ord.values():
                orders_str.append(
                    f'''
Заявка №{i + 1}:
Время заявки: {order['time'].strftime("%Y-%m-%d %H:%M:%S")}
Место посадки: {order['board_dist']} {order['board_street']} {order['board_house']}
Место высадки: {order['drop_dist']} {order['drop_street']} {order['drop_house']}
Клиент: {order['client']}
Имя клиента: {order['cl_name']}
Сумма: {order['cost']}
Статус: {order['status']}
'''
                )

        model = MyListModel(orders_str)

        # Создайте QListView и свяжите его с моделью данных
        self.order_history.setModel(model)

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

