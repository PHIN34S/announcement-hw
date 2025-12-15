# hello.py
import json
import os
import sqlite3
from datetime import datetime

from announcement_ui import Ui_Form

class HomeworkAnnouncement(QWidget):
    def __init__(self, date_text, time_text):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Access widgets via self.ui
        self.ui.labelDate.setText(f"Date: {date_text}")
        self.ui.labelTime.setText(f"Time: {time_text}")

        self.ui.btnClose.clicked.connect(self.close)
        self.ui.btnRefresh.clicked.connect(self.update_time)
        self.ui.btnAdd.clicked.connect(self.add_homework)
        self.ui.btnDelete.clicked.connect(self.delete_homework)
        self.ui.btnAlarm.clicked.connect(self.set_alarm)
        self.ui.btnDarkMode.clicked.connect(self.toggle_dark_mode)

        self.homeworkList = self.ui.homeworkList


        # Set window icon (optional)
        if os.path.exists("icons/app_icon.png"):
            self.setWindowIcon(QIcon("icons/app_icon.png"))

        # Initial date/time
        self.labelDate.setText(f"Date: {date_text}")
        self.labelTime.setText(f"Time: {time_text}")

        # Notification system
        self.notifier = ToastNotifier()

        # Connect buttons
        self.btnClose.clicked.connect(self.close)
        self.btnRefresh.clicked.connect(self.update_time)
        self.btnAdd.clicked.connect(self.add_homework)
        self.btnDelete.clicked.connect(self.delete_homework)
        self.btnAlarm.clicked.connect(self.set_alarm)
        self.btnDarkMode.clicked.connect(self.toggle_dark_mode)

        # Real-time clock timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # Alarm timer
        self.alarm_time = None
        self.alarm_timer = QTimer(self)
        self.alarm_timer.timeout.connect(self.check_alarm)
        self.alarm_timer.start(1000)

        # Fade-in animation
        self.fade_in()

        # Load homework from file & database
        self.homework_file = "homework.json"
        self.db_file = "homework.db"
        self.init_database()

