# Student Attendance Management System (SAMS) 📚🎓

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

A modern, feature-rich Student Attendance Management System with QR code verification, real-time tracking, and comprehensive analytics.

## 🚀 Features

### ✅ Core Features
- **QR Code Attendance**: Generate and scan QR codes for attendance marking
- **Geolocation Verification**: Ensure students are within campus boundaries
- **Real-time Tracking**: Live attendance monitoring for lecturers
- **Multi-role System**: Separate interfaces for Admin, Lecturer, and Student
- **Attendance Analytics**: Detailed reports and statistics

### 🔐 Authentication & Security
- JWT Token-based authentication
- Role-based access control (RBAC)
- Device fingerprinting for security
- Secure session management

### 📱 Notifications
- Real-time push notifications
- Email notifications
- In-app alerts
- Attendance reminders

## 🏗️ Architecture


## 🛠️ Tech Stack

### Backend
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Celery** - Task queue for async processing
- **Redis** - Caching and message broker
- **JWT** - Authentication

### Frontend
- **React 18.x** - UI library
- **Material-UI** - Component library
- **Redux Toolkit** - State management
- **Axios** - HTTP client
- **React Router** - Navigation

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 14+
- Redis

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\Q

Now let's also set up some useful GitHub files:

```bash
# Create LICENSE file
curl -s -o LICENSE https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/mit.txt
sed -i "s/\[year\]/$(date +%Y)/" LICENSE
sed -i "s/\[fullname\]/Riordan/" LICENSE

# Create .github directory for future CI/CD
mkdir -p .github/workflows

# Create a basic GitHub Actions workflow
cat > .github/workflows/django-tests.yml << 'EOF'
name: Django Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run migrations
      run: |
        cd backend
        python manage.py migrate
      env:
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
        SECRET_KEY: test-secret-key
    
    - name: Run tests
      run: |
        cd backend
        python manage.py test
      env:
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
        SECRET_KEY: test-secret-key
        DEBUG: "False"
