import os
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extensions import db, cache
from models import User, Job, JobApplication
from celery_worker import generate_reports

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403
    
    students = User.query.filter_by(role='student').all()
    companies = User.query.filter_by(role='company').all()

    total_jobs = Job.query.count()
    total_applications = JobApplication.query.count()

    return jsonify({
        'students': [
            {
                'ids': s.ids,
                'name': s.name,
                'email': s.email,
                'is_approved': s.is_approved
            } for s in students
        ],
        'companies': [
            {
                'ids': c.ids,
                'name': c.name,
                'email': c.email,
                'is_approved': c.is_approved
            } for c in companies
        ],
        'total_students': len(students),
        'total_companies': len(companies),
        'total_jobs': total_jobs,
        'total_applications': total_applications
    })

@admin_bp.route('/admin/approve/<int:user_id>', methods=['POST'])
@jwt_required()
def approve_company(user_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user or user.role != 'company':
        return jsonify({'msg': 'Invalid company user'}), 404

    user.is_approved = True
    db.session.commit()
    cache.clear()

    return jsonify({'msg': 'Company approved successfully'})

@admin_bp.route('/admin/toggle/<int:user_id>', methods=['POST'])
@jwt_required()
def toggle_user(user_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    user.is_approved = not user.is_approved
    db.session.commit()
    cache.clear()

    return jsonify({'msg': 'Status updated'})

@admin_bp.route('/admin/jobs', methods=['GET'])
@jwt_required()
@cache.cached(
    timeout=120,
    key_prefix=lambda: f"admin_{get_jwt_identity()}_jobs"
)
def admin_jobs():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    jobs = Job.query.all()
    result = []
    for j in jobs:
        company = User.query.get(j.company_id)
        result.append({
            "id": j.id,
            "title": j.title,
            "location": j.location,
            "salary": j.salary,
            "status": j.status,
            "company_name": company.name if company else "Unknown"
        })

    return jsonify(result)

@admin_bp.route('/admin/applications', methods=['GET'])
@jwt_required()
def admin_get_applications():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    apps = JobApplication.query.all()
    result = []

    for a in apps:
        student = a.student
        student_user = student.user_br
        job = a.job
        company = User.query.get(job.company_id)

        result.append({
            "application_id": a.id,
            "student_name": student_user.name,
            "student_email": student_user.email,
            "job_title": job.title,
            "company_name": company.name if company else "Unknown",
            "status": a.status,
            "interview_date": a.interview_date,
            "interview_link": a.interview_link
        })

    return jsonify(result)

@admin_bp.route('/admin/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_job(job_id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'msg': 'Job not found'}), 404

    JobApplication.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()
    cache.clear()

    return jsonify({'msg': 'Job deleted successfully'}), 200

@admin_bp.route("/admin/download-report/<filename>")
def download_report(filename):
    path = os.path.join("reports", filename)
    return send_file(path, as_attachment=True)

@admin_bp.route("/admin/generate-report")
def trigger_report():
    filename = generate_reports()
    return jsonify({"filename": filename})
