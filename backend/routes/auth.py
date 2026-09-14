from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db, jwt
from models import User

auth_bp = Blueprint("auth", __name__)

@jwt.unauthorized_loader
def missing_token_callback(err):
    return jsonify({"msg": "Missing or invalid token"}), 401

@auth_bp.route('/req', methods=['POST'])
def registration():
    data = request.get_json() or {}
    frontend_name = data.get('name')
    frontend_email = data.get('email')
    frontend_pass = data.get('password')
    dr_role = data.get('role')
    
    if dr_role not in ['student', 'company']:
        return jsonify({'msg': 'Invalid role'}), 400

    if not all([frontend_name, frontend_email, frontend_pass, dr_role]):
        return jsonify({'msg': 'Missing Feilds'}), 400
    
    if dr_role == 'admin':
        return jsonify({'msg': 'Administrator cant be registered'}), 400

    existing_pers = User.query.filter_by(email=frontend_email).first()
    if existing_pers:
        return jsonify({'msg': 'Email ALready Exists'}), 400

    new_user = User(
        name=frontend_name,
        email=frontend_email,
        password=generate_password_hash(frontend_pass),
        role=dr_role,
        is_approved=False if dr_role == 'company' else True
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'msg': 'Registration Successfull',
        'user_id': new_user.ids,
        'role': new_user.role
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Invalid JSON'}), 400

    usr = User.query.filter_by(email=data.get('email')).first()

    if not usr:
        return jsonify({'msg': 'User Not Found'}), 404

    if not check_password_hash(usr.password, data.get('password', '')):
        return jsonify({'msg': 'Incorrect Password'}), 401

    if not usr.is_approved:
        return jsonify({'msg': 'Account not approved yet'}), 403

    access_token = create_access_token(
        identity=str(usr.ids),
        additional_claims={"role": usr.role}
    )
    return jsonify({
        "access_token": access_token,
        "role": usr.role,
        "name": usr.name,
        "user_id": usr.ids
    }), 200
