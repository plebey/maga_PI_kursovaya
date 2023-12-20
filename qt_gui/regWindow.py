# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox
from sqlalchemy import text, select, desc
from models import sql_model


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
        if self.login_e.text() and self.pswd_e.text() and self.fio_e.text() and self.birth_date_e.text() and self.ph_e.text()\
                and self.stage_e.text() and self.car_num_e.text() and self.car_name_e.text()\
                and self.car_color_e.text() and self.car_year_e.text():
            username_to_query = self.login_e.text()
            users_with_desired_username = self.dbconn['sql'].query(sql_model.Driver).filter(
                sql_model.Driver.login == username_to_query).all()
            if users_with_desired_username:
                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Водитель с таким логином уже существует.")
                info_box.setWindowTitle("Ошибка")
                info_box.exec()
            else:
                fio = []
                b_date = self.birth_date_e.text()
                b_date = datetime.strptime(b_date, "%d.%m.%Y").date()
                fio = self.fio_e.text().split()
                last_id = self.dbconn['sql'].query(sql_model.Driver).order_by(desc(sql_model.Driver.id)).first().id

                new_car = sql_model.Car(
                    id=self.car_num_e.text(),
                    name=self.car_name_e.text(),
                    color=self.car_color_e.text(),
                    year=self.car_year_e.text(),
                )

                if len(fio) == 3:
                    new_driver = sql_model.Driver(
                        id=last_id + 1,
                        surname= fio[0],
                        name= fio[1],
                        p_name= fio[2],
                        login=self.login_e.text(),
                        pswd=self.pswd_e.text(),
                        birth_date=b_date,
                        work_exp=self.stage_e.text(),
                        car_id=self.car_num_e.text(),
                        ph_num=self.ph_e.text(),
                        status='Неактивен',
                    )
                elif len(fio) == 2:
                    new_driver = sql_model.Driver(
                        id=last_id + 1,
                        surname=fio[0],
                        name=fio[1],
                        login=self.login_e.text(),
                        pswd=self.pswd_e.text(),
                        birth_date=b_date,
                        work_exp=self.stage_e.text(),
                        car_id=self.car_num_e.text(),
                        ph_num=self.ph_e.text(),
                        status='Неактивен',
                    )
                # Добавьте нового клиента в сессию
                self.dbconn['sql'].add(new_car)
                self.dbconn['sql'].add(new_driver)
                # Закоммитить изменения в базе данных
                self.dbconn['sql'].commit()

                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Аккаунт успешно создан.")
                info_box.setWindowTitle("Успех!")
                info_box.exec()
                self.back_to_login()

        else:
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setText("Пожалуйста, заполните все поля.")
            info_box.setWindowTitle("Ошибка")
            info_box.exec()

    def register_client(self):
        # Выполните запрос к базе данных
        if self.login_e.text() and self.pswd_e.text() and self.name_e.text() and self.ph_e.text():
            username_to_query = self.login_e.text()
            users_with_desired_username = self.dbconn['sql'].query(sql_model.Client).filter(
                sql_model.Client.login == username_to_query).all()
            if users_with_desired_username:
                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Пользователь с таким логином уже существует.")
                info_box.setWindowTitle("Ошибка")
                info_box.exec()
            else:
                last_id = self.dbconn['sql'].query(sql_model.Client).order_by(desc(sql_model.Client.id)).first().id
                new_client = sql_model.Client(
                    id=last_id+1,
                    login=self.login_e.text(),
                    pswd=self.pswd_e.text(),
                    name=self.name_e.text(),
                    ph_num=self.ph_e.text(),
                )
                # Добавьте нового клиента в сессию
                self.dbconn['sql'].add(new_client)
                # Закоммитить изменения в базе данных
                self.dbconn['sql'].commit()

                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Аккаунт успешно создан.")
                info_box.setWindowTitle("Успех!")
                info_box.exec()
                self.back_to_login()

        else:
            info_box = QMessageBox()
            info_box.setIcon(QMessageBox.Icon.Information)
            info_box.setText("Пожалуйста, заполните все поля.")
            info_box.setWindowTitle("Ошибка")
            info_box.exec()


    def driver_selected(self):
        self.driver_checked = True
        self.client_checked = False
        self.fio_l.show()
        self.fio_e.show()
        self.birth_date_l.show()
        self.birth_date_e.show()
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
        self.birth_date_l.hide()
        self.birth_date_e.hide()
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
