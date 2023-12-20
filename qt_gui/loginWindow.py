import sys

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy, QMessageBox

from models import sql_model




# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self, dbconn: dict):
        super().__init__()
        self.dbconn = dbconn

        loadUi("qt_ui/main.ui", self)
        self.not_reged_btn.clicked.connect(self.not_reged_btn_click)
        self.enter_btn.clicked.connect(self.enter_click)
        self.radioDriver.toggled.connect(self.driver_selected)
        self.driver_checked = False
        self.client_checked = True
        self.radioClient.toggled.connect(self.client_selected)
        self.show()

        # Устанавливаем центральный виджет Window.
        # self.setCentralWidget(button)

    def not_reged_btn_click(self):
        from qt_gui import RegWindow
        self.hide()
        self.reg_wind = RegWindow(self.dbconn, self)
        self.reg_wind.show()

    def enter_click(self):
        if self.driver_checked:
            if self.login_e.text() and self.pswd_e.text():
                username_to_query = self.login_e.text()
                users_with_desired_username = self.dbconn['sql'].query(sql_model.Driver).filter(
                    sql_model.Driver.login == username_to_query).all()
                if users_with_desired_username:
                    if users_with_desired_username[0].pswd == self.pswd_e.text():
                        from qt_gui import OrderClientWindow
                        self.hide()
                        self.order_client = OrderClientWindow(self.dbconn, self, users_with_desired_username[0].id)
                        self.order_client.show()
                    else:
                        info_box = QMessageBox()
                        info_box.setIcon(QMessageBox.Icon.Information)
                        info_box.setText("Неверный логин/пароль.")
                        info_box.setWindowTitle("Ошибка")
                        info_box.exec()
                else:
                    info_box = QMessageBox()
                    info_box.setIcon(QMessageBox.Icon.Information)
                    info_box.setText("Пользователя не существует.")
                    info_box.setWindowTitle("Ошибка")
                    info_box.exec()
            else:
                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Пожалуйста, заполните все поля.")
                info_box.setWindowTitle("Ошибка")
                info_box.exec()

        elif self.client_checked:
            if self.login_e.text() and self.pswd_e.text():
                username_to_query = self.login_e.text()
                users_with_desired_username = self.dbconn['sql'].query(sql_model.Client).filter(
                    sql_model.Client.login == username_to_query).all()
                if users_with_desired_username:
                    if users_with_desired_username[0].pswd == self.pswd_e.text():
                        from qt_gui import OrderClientWindow
                        self.hide()
                        self.order_client = OrderClientWindow(self.dbconn, self, users_with_desired_username[0].id)
                        self.order_client.show()
                    else:
                        info_box = QMessageBox()
                        info_box.setIcon(QMessageBox.Icon.Information)
                        info_box.setText("Неверный логин/пароль.")
                        info_box.setWindowTitle("Ошибка")
                        info_box.exec()
                else:
                    info_box = QMessageBox()
                    info_box.setIcon(QMessageBox.Icon.Information)
                    info_box.setText("Пользователя не существует.")
                    info_box.setWindowTitle("Ошибка")
                    info_box.exec()
            else:
                info_box = QMessageBox()
                info_box.setIcon(QMessageBox.Icon.Information)
                info_box.setText("Пожалуйста, заполните все поля.")
                info_box.setWindowTitle("Ошибка")
                info_box.exec()

    def driver_selected(self):
        self.driver_checked = True
        self.client_checked = False

    def client_selected(self):
        self.driver_checked = False
        self.client_checked = True

