# -*- coding: utf-8 -*-
import random
import sys
from datetime import datetime

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model
from models.sql_model import District, Street, Client, TaximetrTariff, Order, OrderService, Taximetr


class DatabaseListenerThread(QThread):
    new_order_signal = pyqtSignal(str)  # Сигнал для передачи новой заявки

    def __init__(self, dbconn: dict, ord_id):
        super().__init__()
        self.dbconn = dbconn
        self.ord_id = ord_id

    def run(self):
        while True:
            if self.isInterruptionRequested():
                break
            order = (
                self.dbconn['sql']
                .query(OrderService.id)
                .filter(OrderService.id == self.ord_id)
                .filter(OrderService.driver_id is not None)
                .first()
            )
            if order:
                self.new_order_signal.emit(f'{order[0]}')
                break
            self.sleep(1)




class OrderClientWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/order_client.ui", self)
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
        self.order_btn.clicked.connect(self.find_order_click)

        self.with_cash = True
        self.with_card = False
        self.radio_with_cash.toggled.connect(self.with_cash_click)
        self.radio_with_card.toggled.connect(self.with_card_click)

        # self.radioDriver.toggled.connect(self.driver_selected)
        # self.driver_checked = False
        # self.radioClient.toggled.connect(self.client_selected)
        # self.back.clicked.connect(self.back_to_login)
        # self.client_checked = True
        # self.show()
        # self.client_selected()
        # self.regButton.clicked.connect(self.register_user)

    def handle_new_order(self, order_id):
        from qt_gui import TripClientWindow
        self.hide()
        self.trip_client = TripClientWindow(self.dbconn, self, self.user_id, order_id)
        self.trip_client.show()

    def with_cash_click(self):
        self.with_cash = True
        self.with_card = False

    def with_card_click(self):
        self.with_cash = False
        self.with_card = True


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

    def add_order_to_db(self, tax_prices: list):
        self.last_id = self.dbconn['sql'].query(sql_model.Order).order_by(desc(sql_model.Order.id)).first().id
        boarding_dist_name = self.from_dist.currentText()
        boarding_st_name = self.from_street.currentText()
        boarding_house = self.from_house.text()
        dest_dist_name = self.to_dist.currentText()
        dest_st_name = self.to_street.currentText()
        dest_house = self.to_house.text()

        boarding_dist_id = (
            self.dbconn['sql']
            .query(District.id)
            .filter(District.name == boarding_dist_name)
            .first()
        )
        boarding_dist_id = boarding_dist_id[0]
        dest_dist_id = (
            self.dbconn['sql']
            .query(District.id)
            .filter(District.name == dest_dist_name)
            .first()
        )
        dest_dist_id = dest_dist_id[0]

        boarding_st_id = (
            self.dbconn['sql']
            .query(Street.id)
            .filter(Street.name == boarding_st_name)
            .first()
        )
        boarding_st_id = boarding_st_id[0]

        dest_st_id = (
            self.dbconn['sql']
            .query(Street.id)
            .filter(Street.name == dest_st_name)
            .first()
        )
        dest_st_id = dest_st_id[0]

        new_order = Order(
            id=self.last_id+1,
            name=self.user_id,
            order_time=datetime.now(),
            boarding_dist_id=boarding_dist_id,
            boarding_st_id=boarding_st_id,
            boarding_house=boarding_house,
            drop_dist_id=dest_dist_id,
            drop_st_id=dest_st_id,
            drop_house=dest_house,
            status='Ожидание',
        )
        self.dbconn['sql'].add(new_order)

        new_serv_ord = OrderService(
            id=self.last_id+1,
        )
        self.dbconn['sql'].add(new_serv_ord)

        for tax in tax_prices:
            new_tax = Taximetr(
                order_service_id=self.last_id+1,
                param_id=tax[0],
                value=tax[2],
            )
            self.dbconn['sql'].add(new_tax)



        # Коммит изменений
        self.dbconn['sql'].commit()

    def find_order_click(self):
        if self.order_btn.text() == 'Заказать':
            client = (
                self.dbconn['sql']
                .query(Client)
                .filter(Client.id == self.user_id)
                .all()
            )
            client = client[0]

            if self.with_card:
                if client.card_num:
                    pass
                else:
                    info_box = QMessageBox()
                    info_box.setIcon(QMessageBox.Icon.Information)
                    info_box.setText("Добавьте карту в профиль.")
                    info_box.setWindowTitle("Ошибка")
                    info_box.exec()
                    return

            if self.from_dist.currentText() and self.from_street.currentText() and self.from_house.text() and \
                self.to_dist.currentText() and self.to_street.currentText() and self.to_house.text():

                taximetr_tariff = (
                    self.dbconn['sql']
                    .query(TaximetrTariff)
                    .all()
                )
                tax_prices = []
                for tariff in taximetr_tariff:
                    tax_prices.append([
                            tariff.id,
                            float(tariff.price),
                            random.uniform(0, 3)
                         ])
                if self.drive_docs_checker.isChecked():
                    tax_prices[3][2] = 1
                else:
                    tax_prices[3][2] = 0
                if self.drive_animals_checker.isChecked():
                    tax_prices[4][2] = 1
                else:
                    tax_prices[4][2] = 0
                cost = 0
                for tax in tax_prices:
                    cost = cost + tax[1]*tax[2]
                cost = round(cost, 2)

                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Question)
                info_box.setText(f'Ваш заказ будет стоить {cost}руб. Заказать?')
                info_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                # Отображаем диалог и получаем результат
                result = info_box.exec()

                # Обрабатываем результат
                if result == QMessageBox.StandardButton.Yes:
                    self.order_btn.setText('Поиск.. Нажмите для отмены')
                    self.add_order_to_db(tax_prices)
                    self.listener_thread = DatabaseListenerThread(self.dbconn, self.last_id + 1)
                    self.listener_thread.new_order_signal.connect(self.handle_new_order)

                    self.listener_thread.start()
                    # TODO: Дописать открытие нового окна с заказом при принятии
                    # TODO: Написать отмену заказа при отсутствии водителя

            else:
                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Заполните все поля адреса.")
                info_box.setWindowTitle("Ошибка")
                info_box.exec()
        else:
            self.listener_thread.requestInterruption()
            order_to_delete = (
                self.dbconn['sql']
                .query(Order)
                .filter(Order.name == self.user_id)
                .filter(Order.status == 'Ожидание')
                .all()
                )
            print(order_to_delete)
            if order_to_delete:
                for order in order_to_delete:
                    print('отменяю')
                    order.status = 'Отменен клиентом'
            self.dbconn['sql'].commit()
            self.order_btn.setText('Заказать')





