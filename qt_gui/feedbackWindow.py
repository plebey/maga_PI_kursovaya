from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi


class FeedbackWindow(QMainWindow):
    def __init__(self, dbconn: dict, logWindow, user_id):
        super().__init__()
        loadUi("qt_ui/feedback_cl.ui", self)
        self.dbconn = dbconn
        self.logWind = logWindow
        self.user_id = user_id