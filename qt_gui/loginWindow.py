import sys

from PyQt6.uic import loadUi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSizePolicy
from qt_gui.regWindow import RegWindow


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self, dbconn: dict):
        super().__init__()
        self.dbconn = dbconn

        loadUi("qt_ui/main.ui", self)
        self.show()
        self.not_reged_btn.clicked.connect(self.not_reged_btn_click)
        # Устанавливаем центральный виджет Window.
        # self.setCentralWidget(button)

    def not_reged_btn_click(self):
        self.hide()
        self.reg_wind = RegWindow(self.dbconn, self)
        self.reg_wind.show()

