import os
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash
from extensions import db, cache
from models import User, Job, JobApplication

company_bp = Blueprint("company", __name__)

@company_bp.route('/company/dashboard', methods=['GET'])
@jwt_required()
def company_dashboard():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    jobs_posted = Job.query.filter_by(
        company_id=user_id,
        status="active"
    ).count()

    candidates_applied = (
        JobApplication.query
        .join(Job)
        .filter(Job.company_id == user_id)
        .count()
    )

    candidates_shortlisted = (
        JobApplication.query
        .join(Job)
        .filter(
            Job.company_id == user_id,
            JobApplication.status.in_(["shortlisted", "interview", "selected"])
        )
        .count()
    )

    return jsonify({
        "jobs_posted": jobs_posted,
        "candidates_applied": candidates_applied,
        "candidates_shortlisted": candidates_shortlisted
    })

@company_bp.route("/company/jobs", methods=["POST"])
@jwt_required()
def create_job():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user.is_approved:
        return jsonify({"msg": "Company not approved"}), 403

    claims = get_jwt()
    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json() or {}
    experience = data.get("experience")

    try:
        experience = int(experience)
        if experience < 0:
            return jsonify({"msg": "Experience must be non-negative"}), 400
    except:
        return jsonify({"msg": "Experience must be an integer"}), 400

    if (
        not data.get("title") or
        not data.get("description") or
        not data.get("skills") or
        not data.get("experience") or
        not data.get("benefits")
    ):
        return jsonify({"msg": "All fields are required"}), 400

    existing_job = Job.query.filter(
        Job.company_id == user_id,
        Job.title.ilike(data["title"].strip()),
        Job.location.ilike(data["location"].strip()),
        Job.skills.ilike(data["skills"].strip())
    ).first()

    if existing_job:
        return jsonify({"msg": "Similar job already exists for this role and location"}), 400

    job = Job(
        title=data["title"],
        location=data["location"],
        salary=data["salary"],
        description=data["description"],
        skills=data.get("skills"),
        experience=experience,
        benefits=data.get("benefits"),
        company_id=user_id
    )

    db.session.add(job)
    db.session.commit()

    cache.clear()
    return jsonify({"msg": "Job created Successfull !!"}), 201

@company_bp.route("/company/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    jobs = Job.query.filter_by(company_id=user_id).all()

    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "location": j.location,
            "salary": j.salary,
            "status": j.status,
            "description": j.description,
            "skills": j.skills,
            "experience": j.experience,
            "benefits": j.benefits,
            "applicants": [],
            "shortlisted": []
        }
        for j in jobs
    ])

@company_bp.route("/company/jobs/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    job = Job.query.filter_by(id=job_id, company_id=user_id).first()

    if not job:
        return jsonify({"msg": "Job not found or not owned by company"}), 404

    db.session.delete(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "msg": "Job deleted successfully",
        "deleted_job_id": job_id
    }), 200

@company_bp.route("/company/jobs/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    job = Job.query.filter_by(id=job_id, company_id=user_id).first()

    if not job:
        return jsonify({"msg": "Job not found"}), 404

    data = request.get_json() or {}

    if "title" in data:
        if not data["title"].strip():
            return jsonify({"msg": "Title cannot be empty"}), 400
        job.title = data["title"].strip()

    if "location" in data:
        job.location = data["location"].strip()

    if "salary" in data:
        try:
            salary = int(data["salary"])
            if salary <= 0:
                return jsonify({"msg": "Salary must be positive"}), 400
            job.salary = salary
        except ValueError:
            return jsonify({"msg": "Salary must be integer"}), 400

    if "description" in data:
        job.description = data["description"].strip()

    if "experience" in data:
        try:
            exp = int(data["experience"])
            if exp < 0:
                return jsonify({"msg": "Experience must be non-negative"}), 400
            job.experience = exp
        except:
            return jsonify({"msg": "Experience must be integer"}), 400
    
    if "skills" in data:
        job.skills = data["skills"].strip()

    if "benefits" in data:
        job.benefits = data["benefits"].strip()

    db.session.commit()
    cache.clear()

    return jsonify({
        "msg": "Job updated successfully",
        "job_id": job.id
    }), 200

@company_bp.route('/company/profile', methods=['GET'])
@jwt_required()
def get_company_profile():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('role') != 'company':
        return jsonify({'msg': 'Unauthorized'}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "name": user.name,
        "email": user.email
    })

@company_bp.route('/company/profile', methods=['PUT'])
@jwt_required()
def update_company_profile():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('role') != 'company':
        return jsonify({'msg': 'Unauthorized'}), 403

    user = db.session.get(User, user_id)
    data = request.get_json() or {}

    if "name" in data:
        name = data["name"].strip()
        if not name:
            return jsonify({"msg": "Company name cannot be empty"}), 400
        user.name = name

    if "email" in data:
        email = data["email"].strip()
        if not email:
            return jsonify({"msg": "Email cannot be empty"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.ids != user.ids:
            return jsonify({"msg": "Email already in use"}), 400

        user.email = email

    if "password" in data and data["password"]:
        if len(data["password"]) < 6:
            return jsonify({"msg": "Password must be at least 6 characters"}), 400
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify({
        "msg": "Profile updated successfully",
        "updated_name": user.name,
        "updated_email": user.email
    }), 200

@company_bp.route("/company/applicants", methods=["GET"])
@jwt_required()
@cache.cached(
    timeout=60,
    key_prefix=lambda: f"company_{get_jwt_identity()}_applicants"
)
def get_company_applicants():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    applications = JobApplication.query.join(Job).filter(
        Job.company_id == user_id
    ).all()

    result = []
    for app in applications:
        student_profile = app.student
        user = student_profile.user_br

        result.append({
            "application_id": app.id,
            "student_name": user.name,
            "department": student_profile.department,
            "cgpa": student_profile.cgpa,
            "resume": student_profile.resume,
            "job_title": app.job.title,
            "job_id": app.job.id,
            "status": app.status,
            "interview_date": app.interview_date,
            "interview_link": app.interview_link
        })

    return jsonify(result)

@company_bp.route("/company/application/<int:app_id>/decision", methods=["POST"])
@jwt_required()
def decide_application(app_id):
    claims = get_jwt()
    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json() or {}
    status = data.get("status")
    feedback = data.get("feedback")

    app = JobApplication.query.get(app_id)
    if not app:
        return jsonify({"msg": "Application not found"}), 404

    app.status = status
    app.feedback = feedback
    db.session.commit()

    cache.clear()
    return jsonify({"msg": "Application updated"})

@company_bp.route("/company/application/<int:app_id>/schedule", methods=["PUT"])
@jwt_required()
def schedule_interview(app_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    application = JobApplication.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    job = Job.query.get(application.job_id)
    if job.company_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    if application.status != "shortlisted":
        return jsonify({"msg": "Only shortlisted candidates can be scheduled"}), 400

    data = request.get_json() or {}
    application.interview_date = data.get("interview_date")
    application.interview_link = data.get("interview_link")
    application.status = "interview"

    db.session.commit()
    cache.clear()
    return jsonify({
        "msg": "Interview scheduled successfully",
        "application_id": application.id
    }), 200

@company_bp.route("/company/shortlisted", methods=["GET"])
@jwt_required()
def get_shortlisted_students():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    apps = JobApplication.query.join(Job).filter(
        Job.company_id == user_id,
        JobApplication.status.in_(["shortlisted", "interview", "offer"])
    ).all()

    result = []
    for a in apps:
        student = a.student
        user = student.user_br

        result.append({
            "application_id": a.id,
            "name": user.name,
            "department": student.department,
            "cgpa": student.cgpa,
            "resume": student.resume,
            "job_title": a.job.title,
            "status": a.status,
            "interview_date": a.interview_date,
            "interview_link": a.interview_link
        })

    return jsonify(result)

@company_bp.route("/company/jobs/<int:job_id>/close", methods=["PUT"])
@jwt_required()
def close_job(job_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    job = Job.query.filter_by(id=job_id, company_id=user_id).first()
    if not job:
        return jsonify({"msg": "Job not found"}), 404

    job.status = "closed"
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Job closed"})

@company_bp.route("/company/jobs/<int:job_id>/open", methods=["PUT"])
@jwt_required()
def open_job(job_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    job = Job.query.filter_by(id=job_id, company_id=user_id).first()
    if not job:
        return jsonify({"msg": "Job not found"}), 404

    job.status = "active"
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Job reopened"})

@company_bp.route("/company/application/<int:app_id>/final", methods=["PUT"])
@jwt_required()
def final_decision(app_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    application = JobApplication.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    job = Job.query.get(application.job_id)
    if job.company_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json() or {}
    decision = data.get("decision")
    offer_letter = data.get("offer_letter")

    if decision not in ["selected", "rejected"]:
        return jsonify({"msg": "Invalid decision"}), 400

    if decision == "selected":
        application.status = "offer"
        application.offer_letter = offer_letter
    else:
        application.status = "rejected"

    db.session.commit()
    cache.clear()
    return jsonify({
        "msg": "Final decision recorded",
        "status": decision
    })

@company_bp.route("/company/application/<int:app_id>/place", methods=["PUT"])
@jwt_required()
def mark_placed(app_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    if claims.get("role") != "company":
        return jsonify({"msg": "Unauthorized"}), 403

    application = JobApplication.query.get(app_id)
    if not application:
        return jsonify({"msg": "Application not found"}), 404

    job = Job.query.get(application.job_id)
    if job.company_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    application.status = "placed"
    db.session.commit()
    cache.clear()

    return jsonify({"msg": "Student marked as placed"})

@company_bp.route("/company/export", methods=["POST"])
@jwt_required()
def company_export():
    user_id = int(get_jwt_identity())
    from celery_worker import export_company_csv
    export_company_csv.delay(user_id)
    return jsonify({"msg": "Export started"})

@company_bp.route("/company/download/<filename>")
def company_download(filename):
    path = os.path.join("exports", filename)
    return send_file(path, as_attachment=True)
