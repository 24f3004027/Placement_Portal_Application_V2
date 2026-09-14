import os
import time
import shutil
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def register_pdf_tasks(celery):
    @celery.task
    def generate_reports():
        from app import app, db
        from models import Job, JobApplication

        with app.app_context():
            print("📊 Generating placement PDF report...")

            jobs = Job.query.all()
            styles = getSampleStyleSheet()

            os.makedirs("reports", exist_ok=True)
            filename = f"reports/placement_report_{int(time.time())}.pdf"

            doc = SimpleDocTemplate(filename)
            elements = []

            elements.append(Paragraph("Placement Report", styles["Title"]))
            elements.append(Spacer(1, 20))

            for job in jobs:
                apps = JobApplication.query.filter_by(job_id=job.id).all()

                total = len(apps)
                selected = len([a for a in apps if a.status == "selected"])
                rejected = len([a for a in apps if a.status == "rejected"])
                shortlisted = len([a for a in apps if a.status == "shortlisted"])

                text = f"""
                Job: {job.title}<br/>
                Location: {job.location}<br/>
                Total Applications: {total}<br/>
                Shortlisted: {shortlisted}<br/>
                Selected: {selected}<br/>
                Rejected: {rejected}<br/><br/>
                """

                elements.append(Paragraph(text, styles["Normal"]))
                elements.append(Spacer(1, 15))

            doc.build(elements)

            print(f"📄 PDF Report generated: {filename}")

            latest_path = "reports/placement_report_latest.pdf"
            shutil.copy(filename, latest_path)

            print("📄 Latest report updated")

            return filename

    return generate_reports
