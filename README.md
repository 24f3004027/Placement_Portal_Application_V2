# 🎓 Placement Portal Application (V2)

A full-stack web application designed to streamline the campus placement process.  
This platform connects **Students**, **Companies**, and **Administrators** through a unified system for authentication, job management, and application tracking.

---

## 🚀 Core Features

### 👨‍🎓 Student
- Secure JWT-based login
- Role-protected dashboard access
- Apply for jobs
- Track application status

### 🏢 Company
- Company account registration
- Admin approval required before activation
- Access to company dashboard
- Manage job applications

### 🛠 Admin
- Predefined admin account
- Approve company registrations
- Role-based dashboard control
- System-level access management

---

## 🔐 Authentication & Authorization

- Password hashing using `werkzeug.security`
- JWT authentication via `flask-jwt-extended`
- Role-based access control:
  - `student`
  - `company`
  - `admin`
- Company accounts require admin approval before login

---

## 🏗 Project Structure

Placement_Portal_Application_V2/
│
├── backend/
│ ├── app.py
│ ├── instance/ 
|
├── frontend/
│ ├── src/
│ ├── package.json
│ ├── package-lock.json
│ ├── vite.config.js
│
├── requirements.txt
├── README.md
└── .gitignore


---

## 🧰 Tech Stack

### Backend
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- SQLite (Development)

### Frontend
- Vue 3
- Vite
- Axios

---

## ⚙️ Backend Setup

### 1️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt