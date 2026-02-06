from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Making the Flask and SQLALchemy Instances
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


#The Tables - User Table , Student_Profile Table , Company_Profile Table & Job_Applications Table
class User(db.Model):
    ids = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False)
    #Forward Rel^nship
    student_prf_frwrel = db.relationship("StudentProfile", back_populates = "user_br")

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #Fetch the Administer's Details
        existing_admin = User.query.filter_by(name = "admin").first()
        #If there's no Admin Create it with Hardcoded Predefined Values
        if not existing_admin:
            admin_db = User(
                name = 'admin',
                password = 'admin123',
                email = 'admin@gmail.com',
                role = 'Administer'
            )
            db.session.add(admin_db)
            db.session.commit()

app.run(debug = True)