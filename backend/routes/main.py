import os
from flask import Blueprint, send_file, jsonify
from flask_mail import Message
from extensions import mail
from celery_worker import generate_reports

main_bp = Blueprint("main", __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return 'this is the index page'

@main_bp.route("/reports/<filename>", methods=["GET"])
def get_report(filename):
    path = os.path.join("reports", filename)
    return send_file(path, as_attachment=True)

@main_bp.route("/test-mail")
def test_mail():
    try:
        msg = Message(
            subject="Test Email 🚀",
            recipients=["portalplacement3@gmail.com"],
            body="If you see this, your Placement Portal email system works!"
        )
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return str(e)
