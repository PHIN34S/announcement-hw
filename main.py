# main.py
import sys
from PyQt6.QtWidgets import QApplication
from datetime import datetime
from hello import HomeworkAnnouncement
from database import init_database

if __name__ == "__main__":
    # Initialize SQLite database
    init_database()

    app = QApplication(sys.argv)

    # Get current date and time
    now = datetime.now()
    date_text = now.strftime("%A, %B %d, %Y")
    time_text = now.strftime("%I:%M:%S %p")

    # Create main window
    window = HomeworkAnnouncement(date_text, time_text)

    # Show window
    window.show()

    # Execute application (PyQt6)
    sys.exit(app.exec())
