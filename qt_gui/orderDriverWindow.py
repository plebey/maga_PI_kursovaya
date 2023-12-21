# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import District, Street, Driver, Order


class DatabaseListenerThread(QThread):
    new_order_signal = pyqtSignal(str)  # Сигнал для передачи новой заявки

    def __init__(self, dbconn: dict):
        super().__init__()
        self.dbconn = dbconn

    def run(self):
        while True:
            if self.isInterruptionRequested():
                break
            order = (
                self.dbconn['sql']
                .query(Order.id)
                .filter(Driver.district_now == Order.boarding_dist_id)
                .filter(Order.status == 'Ожидание')
                .first()
            )
            if order:
                self.new_order_signal.emit(f'{order[0]}')
                break
            self.sleep(1)


class OrderDriverWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/order_driver.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id

        self.find_ready = False
        self.account_btn.clicked.connect(self.account_btn_click)
        self.story_btn.clicked.connect(self.history_btn_click)
        self.start_find_btn.clicked.connect(self.start_find_click)

        self.listener_thread = DatabaseListenerThread(dbconn)
        self.listener_thread.new_order_signal.connect(self.handle_new_order)

        # self.radioDriver.toggled.connect(self.driver_selected)
        # self.driver_checked = False
        # self.radioClient.toggled.connect(self.client_selected)
        # self.back.clicked.connect(self.back_to_login)
        # self.client_checked = True
        # self.show()
        # self.client_selected()
        # self.regButton.clicked.connect(self.register_user)

    def handle_new_order(self, order_id):
        self.start_find_click()
        order = (
            self.dbconn['sql']
            .query(Order)
            .filter(Order.id == order_id)
            .filter(Order.status == 'Ожидание')
            .first()
        )
        if order:
            cost = 0
            for tax in order.order_service[0].taximetr:
                cost = cost + tax.value*tax.param.price
            cost = round(cost, 2)
            cost = float(cost) * 0.9

            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Question)
            info_box.setText(f'''
Заказ номер: {order_id}
Детали заказа:
Из: {order.boarding_dist.name} {order.boarding_st.name} {order.boarding_house}
В: {order.drop_dist.name} {order.drop_st.name} {order.drop_house}
Сумма: {cost}
Берём?
''')
            info_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            # Отображаем диалог и получаем результат
            result = info_box.exec()

            # Обрабатываем результат
            if result == QMessageBox.StandardButton.Yes:
                order.order_service[0].driver_id = self.user_id
                print(order.order_service[0].driver_id)
                order.status = 'Обслуживается'
                self.dbconn['sql'].commit()
                # TODO: Вызвать новое окно заказа
                self.hide()
                self.account_driver = AccountDriverWindow(self.dbconn, self, self.user_id)
                self.account_driver.show()
                pass
        else:
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setText("Заказ был отменен или взят другим водителем.")
            info_box.setWindowTitle("Ошибка")
            info_box.exec()



    def account_btn_click(self):
        from qt_gui import AccountDriverWindow
        self.hide()
        self.account_driver = AccountDriverWindow(self.dbconn, self, self.user_id)
        self.account_driver.show()

    def history_btn_click(self):
        from qt_gui import HistoryDriverWindow
        self.hide()
        self.history_driver = HistoryDriverWindow(self.dbconn, self, self.user_id)
        self.history_driver.show()

    def start_find_click(self):
        if not self.find_ready:
            self.find_ready = True
            self.find_label.setText('Поиск заказа')

            driver = (
                self.dbconn['sql']
                .query(Driver)
                .filter(Driver.id == self.user_id)
                .first()
            )
            driver.status = 'Активен'
            self.dbconn['sql'].commit()
            self.listener_thread.start()

        else:
            self.listener_thread.requestInterruption()
            self.find_ready = False
            self.find_label.setText('Найти заказ')
            driver = (
                self.dbconn['sql']
                .query(Driver)
                .filter(Driver.id == self.user_id)
                .first()
            )
            driver.status = 'Неактивен'
            self.dbconn['sql'].commit()

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



