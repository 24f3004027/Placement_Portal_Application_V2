from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

#Making the Flask and SQLALchemy Instances
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db = SQLAlchemy(app)
jwt = JWTManager(app)

#The Tables - User Table , Student_Profile Table , Company_Profile Table & Job_Applications Table
class User(db.Model):
    ids = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(255), nullable = False)
    is_approved = db.Column(db.Boolean, default=True)
    #Forward Rel^nship
    student_prf_frwrel = db.relationship("StudentProfile", back_populates = "user_br" , uselist=False)

class StudentProfile(db.Model):
    __tablename__ = 'student'
    p_id = db.Column(db.Integer , primary_key = True)
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    resume = db.Column(db.Text)
    #one to One Rel^n
    user_id = db.Column(db.Integer, db.ForeignKey("user.ids"), unique = True)
    #Back Relationship
    user_br = db.relationship("User", back_populates = "student_prf_frwrel")

class CompanyProfile(db.Model):
    __tablename__ = 'company'
    c_id = db.Column(db.Integer , primary_key = True)
    company_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)
    # One-to-one with User (Company user)
    user_id = db.Column(db.Integer, db.ForeignKey("user.ids"), unique=True, nullable=False)
    user_br = db.relationship("User")
    # One-to-many with Job_Application
    job_applications = db.relationship("Job_Application", back_populates="company_br")

class Job_Application(db.Model):
    __tablename__ = 'job_application'
    a_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(150), nullable=False)

    # Many-to-one with Student
    student_id = db.Column(db.Integer, db.ForeignKey("student.p_id"), nullable=False)
    student_br = db.relationship("StudentProfile")

    # Many-to-one with Company thereby Creating the Many to Many Relation
    company_id = db.Column(db.Integer, db.ForeignKey("company.c_id"), nullable=False)
    company_br = db.relationship("CompanyProfile", back_populates="job_applications")


@app.route('/',methods = ['GET','POST'])
def index():
    return 'this is the index page'

@app.route('/req',methods = ['POST'])
def registration():
    data = request.get_json()
    frontend_name = data.get('name')
    frontend_email = data.get('email')
    frontend_pass = data.get('password')
    dr_role = data.get('role')
    existing_pers = User.query.filter_by(email = frontend_email).first()

    #Removing The Roles Other than Student and Company
    if dr_role not in ['student', 'company']:
        return jsonify({'msg': 'Invalid role'}), 400

    #check Partial Registration Here 
    if not all([frontend_name, frontend_email, frontend_pass, dr_role]):
        return jsonify({'msg' : 'Missing Feilds'}),400
    
    #Check Admin Registration Here
    if dr_role == 'admin':
        return jsonify({'msg' : 'Administrator cant be registered'}),400

    #If the Person is Already Registered
    if existing_pers:
        return jsonify({'msg' : 'Email ALready Exists '}),400

    new_user = User(
        name = frontend_name,
        email = frontend_email,
        password = generate_password_hash(frontend_pass),
        role = dr_role,
        is_approved = False if dr_role == 'company' else True
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'msg' : 'Registration Successfull',
        'user_id' : new_user.ids,
        'role' : new_user.role
    }),201

@app.route('/login',methods = ['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'msg': 'Invalid JSON'}), 400

    usr = User.query.filter_by(email = data['email']).first()

    #If User Not Found
    if not usr:
        return jsonify({'msg' : 'User Not Found'}),404

    #If Password is Wrong
    if not check_password_hash(usr.password, data['password']):
        return jsonify({'msg': 'Incorrect Password'}), 401

    
    #If User isnt Approved As of Yet
    if not usr.is_approved:
        return jsonify({'msg': 'Account not approved yet'}), 403

    access_token = create_access_token(
        identity = usr.ids,
        additional_claims = {"role": usr.role}
    )
    return jsonify({
        "msg": 'Login Successful',
        "access_token": access_token,
        "role": usr.role
    }), 200

@app.route('/student/dashboard' , methods = ['GET'])
@jwt_required()
def student_dashboard():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims['role'] != 'student':
        return jsonify({
            'msg': 'Unauthorized'
        }), 403
    
    return jsonify({
        'msg': 'Welcome Student',
        'user_id' : user_id
    })

@app.route('/admin/dashboard' , methods = ['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims['role'] != 'admin':
        return jsonify({
            'msg': 'Unauthorized'
        }), 403
    
    return jsonify({
        'msg': 'Welcome Admin',
        'user_id' : user_id
    })

@app.route('/company/dashboard', methods=['GET'])
@jwt_required()
def company_dashboard():
    user_id = get_jwt_identity()
    claims = get_jwt()

    if claims['role'] != 'company':
        return jsonify({'msg': 'Unauthorized'}), 403

    return jsonify({
        'msg': 'Welcome Company',
        'user_id': user_id
    })

#Admin Will Approve the Company
@app.route('/admin/approve/<int:user_id>', methods=['POST'])
@jwt_required()
def approve_company(user_id):
    claims = get_jwt()

    if claims['role'] != 'admin':
        return jsonify({'msg': 'Unauthorized'}), 403

    user = User.query.get(user_id)

    if not user or user.role != 'company':
        return jsonify({'msg': 'Invalid company user'}), 404

    user.is_approved = True
    db.session.commit()

    return jsonify({'msg': 'Company approved successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #Fetch the Administer's Details
        existing_admin = User.query.filter_by(role = "admin").first()
        #If there's no Admin Create it with Hardcoded Predefined Values
        if not existing_admin:
           admin_db = User(
            name='admin',
            password=generate_password_hash('admin123'),
            email='admin@gmail.com',
            role='admin',
            is_approved=True
            )
           db.session.add(admin_db)
           db.session.commit()

app.run(debug = True)