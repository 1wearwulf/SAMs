# SAMS (Student Attendance Management System) - System Architecture Documentation

## Overview

The Student Attendance Management System (SAMS) is a comprehensive solution designed to streamline attendance tracking in educational institutions. The system employs QR code scanning, geofencing, and device fingerprinting to ensure secure and accurate attendance recording while preventing fraudulent activities.

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │   Mobile App    │    │     Backend     │
│   (React)       │◄──►│ (Expo/React Native)│◄──►│   (Django)      │
│                 │    │                 │    │                 │
│ - Admin UI      │    │ - QR Scanning   │    │ - REST API      │
│ - Analytics     │    │ - Geolocation   │    │ - Database      │
│ - Management    │    │ - Notifications │    │ - Security      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │   (PostgreSQL)  │
                    └─────────────────┘
```

### Component Interactions

1. **Web Dashboard ↔ Backend**: RESTful API communication for CRUD operations, analytics data retrieval, and real-time updates
2. **Mobile App ↔ Backend**: RESTful API for attendance marking, authentication, and push notifications via FCM
3. **Backend ↔ Database**: ORM-based data persistence with PostgreSQL
4. **Cross-Component**: Shared authentication tokens, standardized API responses

## Technology Stack

### Backend (Django REST Framework)
- **Framework**: Django 4.2.13 with Django REST Framework
- **Database**: PostgreSQL with Django ORM
- **Authentication**: JWT (JSON Web Tokens) via djangorestframework-simplejwt
- **Caching**: Redis for session and data caching
- **Task Queue**: Celery with Redis broker for background tasks
- **Push Notifications**: Firebase Cloud Messaging (FCM)
- **Security**: Device fingerprinting, geofencing, OTP validation
- **Additional Libraries**:
  - django-cors-headers: Cross-origin resource sharing
  - django-celery-beat: Periodic task scheduling
  - python-decouple: Environment variable management

### Mobile App (Expo/React Native)
- **Framework**: Expo ~54.0.26 with React Native 0.81.5
- **State Management**: Redux Toolkit and Zustand
- **Navigation**: Expo Router ~6.0.16
- **Networking**: Axios for HTTP requests
- **Local Storage**: Expo Secure Store
- **QR Scanning**: Expo Barcode Scanner
- **Location Services**: Expo Location
- **Push Notifications**: Firebase Cloud Messaging
- **Device Info**: Expo Device for fingerprinting
- **UI Components**: React Native Paper and Expo Vector Icons

### Web Dashboard (React)
- **Framework**: React 18.2.0 with React Router DOM 6.14.2
- **State Management**: Redux Toolkit 1.9.5 with multiple slices
- **UI Library**: Material-UI (MUI) 5.14.0
- **HTTP Client**: Axios 1.4.0 for API communication
- **Charts**: Recharts 2.8.0 for data visualization
- **Forms**: Formik 2.4.1 with Yup 1.2.0 validation
- **Styling**: Tailwind CSS 3.3.3
- **QR Generation**: react-qr-code 2.0.10
- **Date Handling**: Moment.js 2.29.4 and react-datepicker 4.16.0
- **Additional Libraries**: React Table 7.8.0, React Toastify 9.1.3

### Alternative Frontend (React)
- **Framework**: React 19.2.1 with React Router DOM 7.10.0
- **UI Library**: Material-UI (MUI) 6.5.0 with Emotion
- **HTTP Client**: Axios 1.13.2 for API communication
- **Testing**: Jest and React Testing Library

## Project Structure

```
sams-project/
├── backend/                          # Django Backend
│   ├── api/                          # Main API application
│   │   ├── apps/                     # Django apps
│   │   │   ├── accounts/             # User management
│   │   │   ├── attendance/           # Attendance logic
│   │   │   │   ├── models.py         # Database models
│   │   │   │   ├── views.py          # API views
│   │   │   │   ├── serializers.py    # Data serialization
│   │   │   │   ├── services/         # Business logic
│   │   │   │   │   ├── otp_service.py
│   │   │   │   │   └── anti_cheat.py
│   │   │   │   └── urls.py           # URL routing
│   │   │   ├── courses/              # Course management
│   │   │   ├── notifications/        # Notification system
│   │   │   ├── analytics/            # Analytics and reporting
│   │   │   └── devices/              # Device management
│   │   ├── permissions.py            # Custom permissions
│   │   ├── serializers.py            # Shared serializers
│   │   ├── urls.py                   # Main API URLs
│   │   └── utils.py                  # Utility functions
│   ├── core/                         # Core functionality
│   │   ├── constants.py              # System constants
│   │   ├── exceptions.py             # Custom exceptions
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── request_logging.py    # Request logging
│   │   │   └── device_check.py       # Device validation
│   │   └── models.py                 # Core models
│   ├── utils/                        # Utility modules
│   │   ├── geolocation.py            # Geolocation utilities
│   │   └── device_fingerprint.py     # Device fingerprinting
│   ├── sams/                         # Django project settings
│   │   ├── settings/                 # Environment-specific settings
│   │   │   ├── base.py               # Base settings
│   │   │   ├── development.py        # Development settings
│   │   │   └── test.py               # Test settings
│   │   ├── urls.py                   # Project URLs
│   │   └── wsgi.py                   # WSGI configuration
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Docker configuration
│   └── manage.py                     # Django management script
├── mobile-app/                       # Flutter Mobile App
│   ├── lib/                          # Dart source code
│   │   ├── core/                     # Core utilities
│   │   │   ├── constants.dart        # App constants
│   │   │   └── routes.dart           # App routing
│   │   ├── models/                   # Data models
│   │   │   ├── attendance.dart       # Attendance model
│   │   │   └── notification.dart     # Notification model
│   │   ├── services/                 # Business logic
│   │   │   ├── auth_service.dart     # Authentication
│   │   │   └── notification_service.dart # Notifications
│   │   ├── providers/                # State management
│   │   │   └── attendance_provider.dart # Attendance state
│   │   └── ui/                       # User interface
│   │       ├── screens/              # App screens
│   │       │   ├── login_screen.dart
│   │       │   └── scan_qr_screen.dart
│   │       └── widgets/              # Reusable widgets
│   ├── android/                      # Android configuration
│   ├── ios/                          # iOS configuration
│   ├── pubspec.yaml                  # Flutter dependencies
│   ├── README.md                     # Mobile app documentation
│   └── build-apk.sh                  # APK build script
├── web-dashboard/                    # React Web Dashboard
│   ├── public/                       # Static assets
│   ├── src/                          # React source code
│   │   ├── components/               # React components
│   │   │   ├── auth/                 # Authentication components
│   │   │   ├── dashboard/            # Dashboard components
│   │   │   ├── attendance/           # Attendance management
│   │   │   ├── courses/              # Course management
│   │   │   ├── students/             # Student management
│   │   │   ├── analytics/            # Analytics components
│   │   │   └── layout/               # Layout components
│   │   ├── contexts/                 # React contexts
│   │   │   └── AuthContext.js        # Authentication context
│   │   ├── services/                 # API services
│   │   │   └── api.js                # Axios API client
│   │   ├── store/                    # Redux store
│   │   │   ├── index.js              # Store configuration
│   │   │   └── slices/               # Redux slices
│   │   │       ├── attendanceSlice.js
│   │   │       ├── coursesSlice.js
│   │   │       ├── studentsSlice.js
│   │   │       └── notificationsSlice.js
│   │   ├── App.js                    # Main App component
│   │   └── index.js                  # App entry point
│   ├── package.json                  # Node dependencies
│   └── Dockerfile                    # Docker configuration
├── deployment/                       # Deployment configurations
│   ├── kubernetes/                   # Kubernetes manifests
│   └── nginx/                        # Nginx configurations
├── docs/                             # Documentation
├── TODO.md                           # Project roadmap
├── TESTING.md                        # Testing guide
├── start.sh                          # Development startup script
└── .gitignore                        # Git ignore rules
```

## Core Features and Functionalities

### 1. User Management
- **Student Registration**: Account creation with email verification
- **Lecturer/Admin Accounts**: Role-based access control
- **Profile Management**: User information updates
- **Authentication**: JWT-based secure login/logout

### 2. Course Management
- **Course Creation**: Define courses with metadata
- **Student Enrollment**: Assign students to courses
- **Schedule Management**: Course timing and location
- **Course Analytics**: Attendance statistics per course

### 3. Attendance System
- **QR Code Generation**: Dynamic QR codes for sessions
- **Geofencing**: Location-based attendance validation
- **Device Fingerprinting**: Prevent device spoofing
- **OTP Verification**: Additional security layer
- **Real-time Tracking**: Live attendance monitoring

### 4. Security Features
- **Anti-cheating Mechanisms**:
  - GPS location validation
  - Device fingerprint verification
  - Time-based session windows
  - OTP expiration
- **Rate Limiting**: API request throttling
- **CORS Configuration**: Secure cross-origin requests
- **Request Logging**: Comprehensive audit trails

### 5. Notification System
- **Push Notifications**: Firebase Cloud Messaging
- **In-app Notifications**: Real-time alerts
- **Email Notifications**: Administrative alerts
- **Scheduled Notifications**: Automated reminders

### 6. Analytics and Reporting
- **Attendance Statistics**: Course-wise and student-wise metrics
- **Trend Analysis**: Historical attendance patterns
- **Export Capabilities**: CSV/PDF report generation
- **Real-time Dashboards**: Live data visualization

## Database Models and Relationships

### Core Models

```python
# User Model (Django Auth User extended)
class User:
    - username: CharField
    - email: EmailField
    - first_name: CharField
    - last_name: CharField
    - role: CharField (student/lecturer/admin)
    - device_fingerprint: JSONField

# Course Model
class Course:
    - name: CharField
    - code: CharField (unique)
    - description: TextField
    - lecturer: ForeignKey(User)
    - students: ManyToManyField(User)
    - schedule: JSONField

# Attendance Session Model
class AttendanceSession:
    - course: ForeignKey(Course)
    - lecturer: ForeignKey(User)
    - qr_code: CharField
    - location: JSONField (lat, lng, radius)
    - start_time: DateTimeField
    - end_time: DateTimeField
    - otp: CharField
    - status: CharField (active/expired)

# Attendance Record Model
class AttendanceRecord:
    - session: ForeignKey(AttendanceSession)
    - student: ForeignKey(User)
    - timestamp: DateTimeField
    - location: JSONField
    - device_info: JSONField
    - status: CharField (present/absent/proxy)

# Notification Model
class Notification:
    - user: ForeignKey(User)
    - title: CharField
    - message: TextField
    - type: CharField
    - read: BooleanField
    - created_at: DateTimeField
```

### Relationships
- **User** ↔ **Course**: Many-to-Many (students enrolled in courses)
- **User** ↔ **AttendanceSession**: One-to-Many (lecturer creates sessions)
- **AttendanceSession** ↔ **AttendanceRecord**: One-to-Many (session has multiple records)
- **User** ↔ **Notification**: One-to-Many (user receives notifications)

## API Endpoints and Services

### Authentication Endpoints
```
POST /api/accounts/register/          # User registration
POST /api/accounts/login/             # User login
POST /api/accounts/logout/            # User logout
POST /api/accounts/refresh/           # Token refresh
GET  /api/accounts/profile/           # Get user profile
PUT  /api/accounts/profile/           # Update user profile
```

### Course Management Endpoints
```
GET    /api/courses/                  # List courses
POST   /api/courses/                  # Create course
GET    /api/courses/{id}/             # Get course details
PUT    /api/courses/{id}/             # Update course
DELETE /api/courses/{id}/             # Delete course
POST   /api/courses/{id}/enroll/      # Enroll student
```

### Attendance Endpoints
```
GET    /api/attendance/sessions/      # List sessions
POST   /api/attendance/sessions/      # Create session
GET    /api/attendance/sessions/{id}/ # Get session details
GET    /api/attendance/qr/{id}/       # Get QR code
POST   /api/attendance/mark/          # Mark attendance
GET    /api/attendance/history/       # Get attendance history
```

### Analytics Endpoints
```
GET /api/analytics/dashboard/         # Dashboard statistics
GET /api/analytics/courses/{id}/      # Course analytics
GET /api/analytics/students/{id}/     # Student analytics
GET /api/analytics/reports/           # Generate reports
```

### Notification Endpoints
```
GET  /api/notifications/              # List notifications
POST /api/notifications/              # Send notification
PUT  /api/notifications/{id}/read/    # Mark as read
```

## Security and Anti-Cheating Mechanisms

### 1. Device Fingerprinting
- **Implementation**: Collects device-specific information (OS, browser, screen resolution, etc.)
- **Purpose**: Prevents students from using multiple devices or spoofing identities
- **Storage**: JSON field in User model with hashed fingerprints

### 2. Geofencing
- **Implementation**: GPS coordinate validation with configurable radius
- **Purpose**: Ensures students are physically present at the lecture location
- **Accuracy**: Within 100 meters by default, configurable per session

### 3. OTP Verification
- **Implementation**: Time-based one-time passwords with 5-minute expiration
- **Purpose**: Additional security layer beyond QR scanning
- **Generation**: Server-side generation with secure random algorithms

### 4. Session Time Windows
- **Implementation**: Strict start/end times for attendance sessions
- **Purpose**: Prevents early or late attendance marking
- **Validation**: Server-side timestamp verification

### 5. Request Throttling
- **Implementation**: Rate limiting on API endpoints
- **Limits**: 100 requests/hour for anonymous, 1000/hour for authenticated users
- **Purpose**: Prevents brute force attacks and abuse

## Deployment and Scaling Considerations

### Development Environment
- **Local Setup**: Docker Compose for all services
- **Database**: SQLite for development, PostgreSQL for production
- **Cache**: Local memory cache for development
- **Notifications**: Console logging for development

### Production Environment
- **Containerization**: Docker containers for all components
- **Orchestration**: Kubernetes for scaling and management
- **Load Balancing**: Nginx reverse proxy with SSL termination
- **Database**: PostgreSQL cluster with read replicas
- **Cache**: Redis cluster for session and data caching
- **CDN**: Static asset delivery via CDN
- **Monitoring**: Application performance monitoring

### Scaling Strategies
- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Database Scaling**: Read/write splitting, connection pooling
- **Caching Layer**: Redis for frequently accessed data
- **Background Tasks**: Celery workers for heavy computations
- **Microservices**: Potential split of analytics and notification services

## Areas for Future AI-Driven Improvements

### 1. Predictive Analytics
- **Attendance Prediction**: ML models to predict attendance patterns
- **Early Warning System**: Identify students at risk of low attendance
- **Optimal Scheduling**: AI-powered course scheduling optimization

### 2. Computer Vision Integration
- **Facial Recognition**: Alternative to QR codes for attendance marking
- **Crowd Detection**: Automated attendance counting in large lectures
- **Behavioral Analysis**: Detect suspicious attendance patterns

### 3. Natural Language Processing
- **Smart Notifications**: Context-aware notification generation
- **Chatbot Support**: AI-powered student assistance
- **Automated Feedback**: NLP analysis of course feedback

### 4. Advanced Security
- **Anomaly Detection**: ML-based fraud detection
- **Behavioral Biometrics**: Keystroke and touch pattern analysis
- **Risk Scoring**: Dynamic security measures based on user behavior

### 5. Intelligent Automation
- **Auto-scheduling**: AI-optimized attendance session timing
- **Dynamic Geofencing**: Adaptive location validation
- **Personalized Learning**: AI-driven attendance insights for educators

### 6. IoT Integration
- **Smart Classroom**: Integration with IoT devices for automated attendance
- **Wearable Devices**: Smartwatch-based attendance marking
- **Environmental Monitoring**: Classroom condition tracking

### 7. Advanced Analytics
- **Deep Learning Insights**: Complex pattern recognition in attendance data
- **Sentiment Analysis**: Student satisfaction correlation with attendance
- **Predictive Modeling**: Dropout prevention and academic performance prediction

## Development Workflow

### Code Quality
- **Linting**: ESLint for JavaScript/TypeScript, Flake8 for Python, Expo lint for React Native
- **Testing**: Unit tests, integration tests, and end-to-end testing
- **Code Review**: Pull request reviews with automated checks
- **Documentation**: Auto-generated API docs and comprehensive READMEs

### CI/CD Pipeline
- **Automated Testing**: Run test suites on every push
- **Code Quality Checks**: Linting and security scanning
- **Build Automation**: Docker image building and deployment
- **Environment Management**: Separate staging and production environments

### Monitoring and Logging
- **Application Monitoring**: Real-time performance metrics
- **Error Tracking**: Centralized error logging and alerting
- **User Analytics**: Usage patterns and feature adoption tracking
- **Security Monitoring**: Intrusion detection and anomaly alerting

## Conclusion

The SAMS architecture provides a robust, scalable foundation for attendance management with strong security measures and modern development practices. The modular design allows for easy extension and the identified AI improvement areas offer clear paths for future enhancements. This documentation serves as a comprehensive guide for developers and AI systems to understand, maintain, and evolve the system effectively.

For specific implementation details, refer to the component-specific README files and the TESTING.md guide for comprehensive testing procedures.
