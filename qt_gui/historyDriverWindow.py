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
        loadUi("qt_ui/order_history.ui", self)
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
        from qt_gui import AccountClientWindow
        self.hide()
        self.account_client = AccountClientWindow(self.dbconn, self, self.user_id)
        self.account_client.show()

    def order_btn_click(self):
        from qt_gui import OrderClientWindow
        self.hide()
        self.order_client = OrderClientWindow(self.dbconn, self, self.user_id)
        self.order_client.show()

    def update_list_view(self):
        query_result = (
            self.dbconn['sql']
            .query(Client)
            .filter(Client.id == self.user_id)
            .all()
        )
        orders = []
        for elem in query_result:
            for i, order in enumerate(elem.orders):
                for service in order.order_service:
                    price = 0
                    for tax in service.taximetr:
                        price = price + (tax.value * tax.param.price)

                orders.append({order.id: {
                    'time': order.order_time,
                    'board_street': order.boarding_st.name,
                    'board_dist': order.boarding_dist.name,
                    'board_house': order.boarding_house,
                    'drop_street': order.drop_st.name,
                    'drop_dist': order.drop_dist.name,
                    'drop_house': order.drop_house,
                    'status': order.status,
                    'driver': order.order_service[0].driver.name,
                    'car_num': order.order_service[0].driver.car_id,
                    'cost': price,
                }})
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
Водитель: {order['driver']}
Номер авто: {order['car_num']}
Сумма: {order['cost']}
Статус: {order['status']}
'''
                )

        model = MyListModel(orders_str)

        # Создайте QListView и свяжите его с моделью данных
        self.order_history.setModel(model)

