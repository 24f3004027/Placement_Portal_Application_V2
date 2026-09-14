from extensions import db

class User(db.Model):
    ids = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    is_approved = db.Column(db.Boolean, default=True)
    
    student_prf_frwrel = db.relationship("StudentProfile", back_populates="user_br", uselist=False)

class StudentProfile(db.Model):
    __tablename__ = 'student'
    p_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    resume = db.Column(db.Text)
    education = db.Column(db.String(255))
    skills = db.Column(db.String(255))
    experience = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.ids"), unique=True)
    user_br = db.relationship("User", back_populates="student_prf_frwrel")

class CompanyProfile(db.Model):
    __tablename__ = 'company'

    c_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.ids"), unique=True, nullable=False)
    user_br = db.relationship("User")

class Job(db.Model):
    __tablename__ = "job"
    
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.String(255))
    title = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    salary = db.Column(db.Integer)
    description = db.Column(db.Text)
    experience = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey("company.user_id"))
    benefits = db.Column(db.Text)
    status = db.Column(db.String(20), default="active")

class JobApplication(db.Model):
    __tablename__ = "job_application"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey("job.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.p_id"))
    offer_letter = db.Column(db.String(255))
    status = db.Column(db.String(20), default="applied")
    feedback = db.Column(db.Text)
    interview_date = db.Column(db.String(50))
    interview_link = db.Column(db.String(255))
    reminder_sent = db.Column(db.Boolean, default=False)
    
    student = db.relationship("StudentProfile")
    job = db.relationship("Job")
