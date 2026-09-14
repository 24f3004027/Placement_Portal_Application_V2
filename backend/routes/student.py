import os
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from extensions import db, cache
from models import User, StudentProfile, Job, JobApplication
from celery_worker import export_csv

student_bp = Blueprint("student", __name__)

@student_bp.route('/student/dashboard', methods=['GET'])
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('role') != 'student':
        return jsonify({'msg': 'Unauthorized'}), 403
    
    return jsonify({
        'msg': 'Welcome Student',
        'user_id': user_id
    })

@student_bp.route("/student/jobs", methods=["GET"])
@jwt_required()
@cache.cached(
    timeout=60,
    key_prefix=lambda: f"user_{get_jwt_identity()}_jobs",
    query_string=True
)
def student_jobs():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "student":
        return jsonify({"msg": "Unauthorized"}), 403

    jobs = Job.query.join(User, Job.company_id == User.ids).filter(
        Job.status == "active",
        User.is_approved == True
    ).all()

    student = StudentProfile.query.filter_by(user_id=user_id).first()
    applied_job_ids = set(
        a.job_id for a in JobApplication.query.filter_by(student_id=student.p_id).all()
    ) if student else set()

    result = []
    for j in jobs:
        company = User.query.get(j.company_id)
        result.append({
            "id": j.id,
            "title": j.title,
            "location": j.location,
            "salary": j.salary,
            "description": j.description,
            "skills": j.skills,
            "experience": j.experience,
            "benefits": j.benefits,
            "company_name": company.name if company else "Unknown",
            "applied": j.id in applied_job_ids
        })

    return jsonify(result)

@student_bp.route("/student/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_job(job_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "student":
        return jsonify({"msg": "Unauthorized"}), 403

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student profile not found"}), 404

    if not student.cgpa:
        return jsonify({"msg": "Please complete your profile (CGPA required)"}), 400

    existing = JobApplication.query.filter_by(
        job_id=job_id,
        student_id=student.p_id
    ).first()

    if existing:
        return jsonify({"msg": "Already applied"}), 400

    new_app = JobApplication(
        job_id=job_id,
        student_id=student.p_id
    )

    db.session.add(new_app)
    db.session.commit()
    
    cache.delete_memoized(student_applications)
    cache.delete_memoized(student_jobs)
    return jsonify({"msg": "Applied successfully"}), 201

@student_bp.route("/student/applications", methods=["GET"])
@jwt_required()
@cache.cached(
    timeout=30,
    key_prefix=lambda: f"user_{get_jwt_identity()}_applications"
)
def student_applications():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "student":
        return jsonify({"msg": "Unauthorized"}), 403

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        student = StudentProfile(user_id=user_id)
        db.session.add(student)
        db.session.commit()

    apps = JobApplication.query.filter_by(student_id=student.p_id).all()

    result = []
    for a in apps:
        result.append({
            "id": a.id,
            "job_title": a.job.title,
            "job_id": a.job.id,
            "status": a.status,
            "feedback": a.feedback,
            "interview_date": a.interview_date,
            "interview_link": a.interview_link,
            "offer_letter": a.offer_letter
        })

    return jsonify(result)

@student_bp.route("/student/profile", methods=["GET"])
@jwt_required()
def get_student_profile():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "student":
        return jsonify({"msg": "Unauthorized Role"}), 403

    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        student = StudentProfile(user_id=user_id)
        db.session.add(student)

    user = db.session.get(User, user_id)

    if not student:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "education": "",
            "skills": "",
            "experience": "",
            "department": "",
            "cgpa": "",
            "resume": ""
        })

    return jsonify({
        "name": user.name,
        "email": user.email,
        "education": student.education,
        "skills": student.skills,
        "experience": student.experience,
        "department": student.department,
        "cgpa": student.cgpa,
        "resume": student.resume
    })

@student_bp.route("/student/profile", methods=["PUT"])
@jwt_required()
def update_student_profile():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "student":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json() or {}
    user = db.session.get(User, user_id)
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        student = StudentProfile(user_id=user_id)
        db.session.add(student)
        db.session.commit()

    student.education = data.get("education")
    student.skills = data.get("skills")
    student.experience = data.get("experience")

    if "name" in data:
        if not data["name"].strip():
            return jsonify({"msg": "Name cannot be empty"}), 400
        user.name = data["name"]

    if "email" in data:
        email = data["email"].strip()
        if not email:
            return jsonify({"msg": "Email cannot be empty"}), 400

        existing = User.query.filter_by(email=email).first()
        if existing and existing.ids != user.ids:
            return jsonify({"msg": "Email already in use"}), 400

        user.email = email

    if "password" in data and data["password"]:
        if len(data["password"]) < 6:
            return jsonify({"msg": "Password must be at least 6 characters"}), 400
        user.password = generate_password_hash(data["password"])

    student.department = data.get("department")
    student.cgpa = data.get("cgpa")
    student.resume = data.get("resume")

    db.session.add(student)
    db.session.commit()

    cache.clear()
    return jsonify({"msg": "Profile updated successfully"})

@student_bp.route("/student/export", methods=["POST"])
@jwt_required()
def export_data():
    user_id = int(get_jwt_identity())
    student = StudentProfile.query.filter_by(user_id=user_id).first()

    if not student:
        student = StudentProfile(user_id=user_id)
        db.session.add(student)
        db.session.commit()

    filename = export_csv(user_id)

    return jsonify({
        "msg": "Export ready",
        "filename": filename
    })

@student_bp.route("/student/download/<filename>", methods=["GET"])
@jwt_required()
def download_file(filename):
    path = os.path.join("exports", filename)
    return send_file(path, as_attachment=True)
