# alarm.py
from datetime import datetime
from win10toast import ToastNotifier
import os

class AlarmManager:
    def __init__(self, icon_path=None):
        self.alarm_time = None
        self.notifier = ToastNotifier()
        self.icon_path = icon_path if icon_path else None

    def set_alarm(self, time_str):
        """
        Set alarm from string "HH:MM" 24-hour format
        """
        try:
            self.alarm_time = datetime.strptime(time_str, "%H:%M").time()
            return True, f"Alarm set for {self.alarm_time.strftime('%I:%M %p')}"
        except ValueError:
            self.alarm_time = None
            return False, "Invalid time format. Use HH:MM 24-hour format."

    def check_alarm(self):
        """
        Check current time and trigger alarm if match.
        Should be called every second.
        """
        if self.alarm_time:
            now = datetime.now().time()
            if now.hour == self.alarm_time.hour and now.minute == self.alarm_time.minute and now.second == 0:
                self.trigger_alarm()
                # Reset alarm to prevent multiple triggers
                self.alarm_time = None

    def trigger_alarm(self, title="Homework Alarm", message="⏰ It's time to study!"):
        """
        Show Windows notification
        """
        self.notifier.show_toast(
            title,
            message,
            duration=5,
            threaded=True,
            icon_path=self.icon_path if os.path.exists(self.icon_path or "") else None
        )
