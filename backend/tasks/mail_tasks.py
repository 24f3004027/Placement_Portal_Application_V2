from datetime import datetime, timedelta
from flask_mail import Message
from extensions import mail

def register_mail_tasks(celery):
    @celery.task
    def send_interview_reminders():
        from app import app, db
        from models import JobApplication

        with app.app_context():
            now = datetime.now()
            upcoming = now + timedelta(days=1)

            interviews = JobApplication.query.filter(
                JobApplication.interview_date != None
            ).all()

            for i in interviews:
                interview_time = i.interview_date
                if isinstance(interview_time, str):
                    try:
                        interview_time = datetime.fromisoformat(interview_time)
                    except:
                        continue

                if (
                    interview_time and
                    now <= interview_time <= upcoming and
                    not i.reminder_sent
                ):
                    try:
                        recipient_email = i.student.user_br.email if (i.student and i.student.user_br) else None
                        student_name = i.student.user_br.name if (i.student and i.student.user_br) else "Student"
                        job_title = i.job.title if i.job else "Job Opportunity"

                        if recipient_email:
                            msg = Message(
                                subject="Reminder: Interview in 24 Hours",
                                recipients=[recipient_email],
                                body=f"""
                                Hello {student_name},

                                You have an interview scheduled!

                                Job: {job_title}
                                Time: {interview_time}

                                Best of luck!
                                """
                            )
                            mail.send(msg)
                            print(f"📧 Email sent to {recipient_email}")
                            i.reminder_sent = True

                    except Exception as e:
                        print("❌ Email failed:", e)

            db.session.commit()

    def send_email(to, subject, body):
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body
        )
        mail.send(msg)

    return send_interview_reminders, send_email
