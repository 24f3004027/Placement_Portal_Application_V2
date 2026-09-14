from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from config import Config
from extensions import db, jwt, cache, mail
from models import User, StudentProfile, CompanyProfile, Job, JobApplication
from routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)

    register_blueprints(app)

    return app

app = create_app()

def init_admin():
    with app.app_context():
        db.create_all()
        existing_admin = User.query.filter_by(role="admin").first()
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

init_admin()

if __name__ == '__main__':
    app.run(debug=True)