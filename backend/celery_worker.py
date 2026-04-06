import sys
import os
sys.path.append(os.path.dirname(__file__))

from celery import Celery
import csv

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

from celery.schedules import crontab

celery.conf.beat_schedule = {
    "interview-reminder-every-minute": {
        "task": "celery_worker.send_interview_reminders",
        "schedule": 60.0,
    },
    "generate-report-every-2-minutes": {
        "task": "celery_worker.generate_reports",
        "schedule": 120.0,
    }
}

@celery.task
def export_csv(user_id):

    print(f"Exporting CSV for {user_id}")

    from app import app, db, JobApplication, StudentProfile

    with app.app_context():

        student = StudentProfile.query.filter_by(user_id=user_id).first()

        if not student:
            return

        apps = JobApplication.query.filter_by(student_id=student.p_id).all()

        import csv
        import time
        filename = f"exports/export_{user_id}_{int(time.time())}.csv"

        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Job Title", "Status"])

            for a in apps:
                writer.writerow([a.job.title, a.status])

        print(f"{filename} generated")

@celery.task
@celery.task
def send_interview_reminders():
    from app import db, app, JobApplication
    from datetime import datetime, timedelta

    with app.app_context():
        now = datetime.now()
        upcoming = now + timedelta(minutes=30)

        interviews = JobApplication.query.filter(
            JobApplication.interview_date != None
        ).all()

        updated = False  

        for i in interviews:
            if (
                i.interview_date and
                now <= i.interview_date <= upcoming and
                not i.reminder_sent
            ):
                print(f"📢 Reminder: {i.job.title} interview at {i.interview_date}")
                i.reminder_sent = True
                updated = True  

        if updated:  
            db.session.commit()

@celery.task
def generate_reports():
    from app import app, db, Job, JobApplication
    import os, json, time

    with app.app_context():
        print("📊 Generating placement reports...")

        jobs = Job.query.all()
        report = {}

        for job in jobs:
            apps = JobApplication.query.filter_by(job_id=job.id).all()

            total = len(apps)
            selected = len([a for a in apps if a.status == "selected"])
            rejected = len([a for a in apps if a.status == "rejected"])
            shortlisted = len([a for a in apps if a.status == "shortlisted"])

            report[job.title] = {
                "total": total,
                "selected": selected,
                "rejected": rejected,
                "shortlisted": shortlisted
            }

        os.makedirs("reports", exist_ok=True)

        filename = f"reports/placement_report_{int(time.time())}.json"

        with open(filename, "w") as f:
            json.dump(report, f, indent=4)

        print(f"📊 Report generated: {filename}")

import celery_worker