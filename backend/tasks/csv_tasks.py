import os
import csv
from datetime import datetime

def register_csv_tasks(celery):
    @celery.task
    def export_csv(user_id):
        from app import app, db
        from models import StudentProfile, JobApplication

        with app.app_context():
            student = StudentProfile.query.filter_by(user_id=user_id).first()
            if not student:
                return None

            apps = JobApplication.query.filter_by(student_id=student.p_id).all()
            os.makedirs("exports", exist_ok=True)
            filepath = f"exports/export_{user_id}.csv"

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Job Title", "Status"])
                for a in apps:
                    writer.writerow([a.job.title if a.job else "N/A", a.status])

            print(f"CSV generated: {filepath}")
            return filepath

    @celery.task
    def export_company_csv(user_id):
        from app import app, db
        from models import Job, JobApplication

        with app.app_context():
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
            os.makedirs(EXPORT_FOLDER, exist_ok=True)
            filepath = os.path.join(EXPORT_FOLDER, f"export_{user_id}.csv")

            jobs = Job.query.filter_by(company_id=user_id).all()

            with open(filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Report Generated At:", str(datetime.now())])
                writer.writerow([])
                writer.writerow([
                    "Job Title",
                    "Location",
                    "Total Applicants",
                    "Shortlisted",
                    "Selected",
                    "Rejected"
                ])

                for job in jobs:
                    apps = JobApplication.query.filter_by(job_id=job.id).all()
                    total = len(apps)
                    shortlisted = len([a for a in apps if a.status == "shortlisted"])
                    selected = len([a for a in apps if a.status == "selected"])
                    rejected = len([a for a in apps if a.status == "rejected"])

                    writer.writerow([
                        job.title,
                        job.location,
                        total,
                        shortlisted,
                        selected,
                        rejected
                    ])

            print("✅ Company CSV generated at:", filepath)
            return filepath

    return export_csv, export_company_csv
