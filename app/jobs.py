import time

from app import app
from app.models import Task

def deliver_notification(task_id: int):
    time.sleep(1)
    with app.app_context():
        task = Task.query.get(task_id)
        if not task:
            print(f"[Worker] Task {task_id} not found")
            return

        print(f"[Worker] Reminder: Task {task.title} is due soon!")
