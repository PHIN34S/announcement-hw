# hello.py
import json
import os
import sqlite3
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QInputDialog, QMessageBox, QListWidgetItem, QFileDialog
)
from win10toast import ToastNotifier   # Windows notifications


class HomeworkAnnouncement(QWidget):
    def __init__(self, date_text, time_text):
        super().__init__()

        # Load UI
        uic.loadUi("announcement.ui", self)

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
        self.load_homework()

        # Dark mode state
        self.dark_mode_enabled = False

    # ------------------------------
    # Fade-In Animation
    # ------------------------------
    def fade_in(self):
        self.setWindowOpacity(0)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(1200)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

    # ------------------------------
    # Time Updates
    # ------------------------------
    def update_time(self):
        now = datetime.now()
        self.labelTime.setText("Time: " + now.strftime("%I:%M:%S %p"))
        self.labelDate.setText("Date: " + now.strftime("%A, %B %d, %Y"))

    # ------------------------------
    # Homework List Functions
    # ------------------------------
    def add_homework(self):
        text, ok = QInputDialog.getText(self, "Add Homework", "Homework Task:")
        if ok and text.strip():
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.homeworkList.addItem(item)
            self.save_homework()

    def delete_homework(self):
        selected = self.homeworkList.currentRow()
        if selected >= 0:
            self.homeworkList.takeItem(selected)
            self.save_homework()

    # ------------------------------
    # JSON Persistence
    # ------------------------------
    def save_homework(self):
        data = []
        for i in range(self.homeworkList.count()):
            item = self.homeworkList.item(i)
            data.append({
                "task": item.text(),
                "checked": item.checkState() == Qt.Checked
            })

        with open(self.homework_file, "w") as f:
            json.dump(data, f, indent=4)

        self.save_to_database(data)

    def load_homework(self):
        if os.path.exists(self.homework_file):
            with open(self.homework_file, "r") as f:
                items = json.load(f)

            for hw in items:
                item = QListWidgetItem(hw["task"])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked if hw["checked"] else Qt.Unchecked)
                self.homeworkList.addItem(item)

    # ------------------------------
    # SQLite Database
    # ------------------------------
    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS homework (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                checked INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_to_database(self, homework_data):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute("DELETE FROM homework")

        for item in homework_data:
            c.execute(
                "INSERT INTO homework (task, checked) VALUES (?, ?)",
                (item["task"], int(item["checked"]))
            )

        conn.commit()
        conn.close()

    # ------------------------------
    # Alarm System
    # ------------------------------
    def set_alarm(self):
        time_str, ok = QInputDialog.getText(
            self, "Set Alarm", "Enter alarm time (HH:MM, 24hr format):"
        )
        if ok:
            try:
                self.alarm_time = datetime.strptime(time_str, "%H:%M").time()
                QMessageBox.information(self, "Alarm Set",
                    f"Alarm set for {self.alarm_time.strftime('%I:%M %p')}")
            except:
                QMessageBox.warning(self, "Invalid Input", "Please use HH:MM format.")

    def check_alarm(self):
        if self.alarm_time:
            now = datetime.now().time()
            if (now.hour == self.alarm_time.hour and
                now.minute == self.alarm_time.minute and
                now.second == 0):
                self.trigger_alarm()

    def trigger_alarm(self):
        self.notifier.show_toast(
            "Homework Alarm",
            "⏰ It's time to study!",
            duration=5,
            threaded=True,
            icon_path="icons/bell.ico" if os.path.exists("icons/bell.ico") else None
        )
        self.alarm_time = None

    # ------------------------------
    # Dark Mode Toggle
    # ------------------------------
    def toggle_dark_mode(self):
        if self.dark_mode_enabled:
            self.set_light_mode()
        else:
            self.set_dark_mode()

        self.dark_mode_enabled = not self.dark_mode_enabled

    def set_dark_mode(self):
        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: #f0f0f0; }
            QPushButton {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                padding: 6px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QListWidget {
                background: #2c2c2c;
                color: white;
                border: 1px solid #555;
            }
        """)

    def set_light_mode(self):
        self.setStyleSheet("""
            QWidget { background-color: #e7f0ff; font-family: Segoe UI; }
            QPushButton {
                background-color: #0056d6;
                color: white;
                padding: 6px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #003f99; }
            QListWidget {
                background: #ffffff;
                border: 1px solid #b0c4de;
            }
        """)
