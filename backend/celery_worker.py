import sys
import os
sys.path.append(os.path.dirname(__file__))

from celery import Celery
from celery.schedules import crontab
from tasks.csv_tasks import register_csv_tasks
from tasks.mail_tasks import register_mail_tasks
from tasks.pdf_tasks import register_pdf_tasks

celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery.conf.beat_schedule = {
    "send-reminders-every-minute": {
        "task": "celery_worker.send_interview_reminders",
        "schedule": crontab(minute="*/1"),
    }
}

export_csv, export_company_csv = register_csv_tasks(celery)
send_interview_reminders, send_email = register_mail_tasks(celery)
generate_reports = register_pdf_tasks(celery)

__all__ = [
    "celery",
    "export_csv",
    "export_company_csv",
    "send_interview_reminders",
    "generate_reports",
    "send_email"
]