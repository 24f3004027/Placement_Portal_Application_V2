from routes.auth import auth_bp
from routes.student import student_bp
from routes.company import company_bp
from routes.admin import admin_bp
from routes.main import main_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
