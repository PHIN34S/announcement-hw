# homework_manager.py
import json
import os
from database import add_homework, delete_homework, update_status, get_all_homework

JSON_FILE = "homework.json"


# -------------------------------------------------------------
# Load homework from JSON file
# -------------------------------------------------------------
def load_homework():
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
            # Validate structure
            for item in data:
                if "task" not in item or "checked" not in item:
                    raise ValueError("Invalid JSON structure")
            return data
        except json.JSONDecodeError:
            return []


# -------------------------------------------------------------
# Save homework to JSON file
# -------------------------------------------------------------
def save_homework(homework_list):
    """
    homework_list: list of dicts [{task: str, checked: bool}]
    """
    with open(JSON_FILE, "w") as f:
        json.dump(homework_list, f, indent=4)

    # Also save to database
    for i, item in enumerate(homework_list):
        # For simplicity, clear all DB entries and re-add
        pass  # handled in hello.py save_to_database()


# -------------------------------------------------------------
# Add a homework item
# -------------------------------------------------------------
def add_task(task, checked=False):
    homework = load_homework()
    homework.append({"task": task, "checked": checked})
    save_homework(homework)
    add_homework(task, checked)


# -------------------------------------------------------------
# Delete a homework item by index
# -------------------------------------------------------------
def delete_task(index):
    homework = load_homework()
    if 0 <= index < len(homework):
        homework.pop(index)
        save_homework(homework)
    # Optionally sync with DB
    db_items = get_all_homework()
    if index < len(db_items):
        delete_homework(db_items[index][0])


# -------------------------------------------------------------
# Update checked status
# -------------------------------------------------------------
def update_task_status(index, checked):
    homework = load_homework()
    if 0 <= index < len(homework):
        homework[index]["checked"] = checked
        save_homework(homework)

    # Also update DB
    db_items = get_all_homework()
    if index < len(db_items):
        update_status(db_items[index][0], checked)
