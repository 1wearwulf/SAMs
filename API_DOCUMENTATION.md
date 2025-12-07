# SAMS Backend API Documentation

## Overview
This document provides comprehensive documentation for the Student Attendance Management System (SAMS) backend API endpoints.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses JWT (JSON Web Token) authentication via `rest_framework_simplejwt`.

### Authentication Headers
All authenticated requests must include:
```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Login
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**: Access and refresh tokens
- **Permissions**: AllowAny

#### Token Refresh
- **URL**: `/api/auth/refresh/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response**: New access token
- **Permissions**: AllowAny

#### Register
- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "role": "student|lecturer|admin"
  }
  ```
- **Response**: User data and tokens
- **Permissions**: AllowAny

## API Endpoints

### Users Management
**Base URL**: `/api/users/`

#### List Users
- **URL**: `GET /api/users/`
- **Permissions**: Authenticated (role-based filtering)
- **Response**: List of users based on requester's role

#### Retrieve User
- **URL**: `GET /api/users/{id}/`
- **Permissions**: Authenticated (role-based access)

#### Current User Profile
- **URL**: `GET /api/users/me/`
- **Permissions**: Authenticated

### Students Management
**Base URL**: `/api/accounts/students/`

#### List Students
- **URL**: `GET /api/accounts/students/`
- **Permissions**: Authenticated (role-based filtering)

#### Retrieve Student
- **URL**: `GET /api/accounts/students/{id}/`
- **Permissions**: Authenticated (role-based access)

#### Current Student Profile
- **URL**: `GET /api/accounts/students/me/`
- **Permissions**: Authenticated (students only)

### Courses Management
**Base URL**: `/api/courses/`

#### List Courses
- **URL**: `GET /api/courses/`
- **Permissions**: Authenticated (role-based filtering)

#### Create Course
- **URL**: `POST /api/courses/`
- **Permissions**: Lecturers and Admins

#### Retrieve Course
- **URL**: `GET /api/courses/{id}/`
- **Permissions**: Authenticated

#### Update Course
- **URL**: `PUT/PATCH /api/courses/{id}/`
- **Permissions**: Lecturers and Admins

#### Delete Course
- **URL**: `DELETE /api/courses/{id}/`
- **Permissions**: Admins

#### Course Actions
- **Enroll**: `POST /api/courses/{id}/enroll/`
- **Unenroll**: `POST /api/courses/{id}/unenroll/`
- **Students List**: `GET /api/courses/{id}/students/`

#### Course Sessions
- **URL**: `GET /api/courses/{id}/sessions/`
- **Permissions**: Authenticated

### Attendance Management
**Base URL**: `/api/attendance/`

#### List Attendance Records
- **URL**: `GET /api/attendance/`
- **Permissions**: Authenticated (role-based filtering)

#### Retrieve Attendance Record
- **URL**: `GET /api/attendance/{id}/`
- **Permissions**: Authenticated (role-based access)

#### Mark Attendance
- **URL**: `POST /api/attendance/mark/`
- **Body**:
  ```json
  {
    "qr_code": "string",
    "latitude": "number (optional)",
    "longitude": "number (optional)",
    "device_fingerprint": "string (optional)"
  }
  ```
- **Permissions**: Students only

#### Verify QR Code
- **URL**: `POST /api/attendance/verify/`
- **Body**:
  ```json
  {
    "code": "string"
  }
  ```
- **Permissions**: Authenticated

### Devices Management
**Base URL**: `/api/devices/`

#### List User Devices
- **URL**: `GET /api/devices/`
- **Permissions**: Authenticated (user's own devices)

#### Register Device
- **URL**: `POST /api/devices/`
- **Permissions**: Authenticated

#### Retrieve Device
- **URL**: `GET /api/devices/{id}/`
- **Permissions**: Authenticated (owner only)

#### Update Device
- **URL**: `PUT/PATCH /api/devices/{id}/`
- **Permissions**: Authenticated (owner only)

#### Delete Device
- **URL**: `DELETE /api/devices/{id}/`
- **Permissions**: Authenticated (owner only)

### Analytics
**Base URL**: `/api/analytics/`

#### Attendance Analytics
- **URL**: `GET /api/analytics/attendance-analytics/`
- **Permissions**: Authenticated

#### Student Analytics
- **URL**: `GET /api/analytics/student-analytics/`
- **Permissions**: Authenticated

#### Lecturer Analytics
- **URL**: `GET /api/analytics/lecturer-analytics/`
- **Permissions**: Authenticated

#### System Analytics
- **URL**: `GET /api/analytics/system-analytics/`
- **Permissions**: Authenticated

#### Dashboard
- **URL**: `GET /api/analytics/dashboard/`
- **Permissions**: Authenticated

#### Reports
- **URL**: `GET /api/analytics/reports/`
- **Permissions**: Authenticated

### Reports
**Base URL**: `/api/reports/`

#### Attendance Report
- **URL**: `GET /api/reports/attendance/`
- **Query Parameters**:
  - `course_id`: Filter by course
  - `session_id`: Filter by session
  - `start_date`: Start date filter
  - `end_date`: End date filter
- **Permissions**: Authenticated

## User Roles and Permissions

### Student
- View own profile and attendance
- Enroll/unenroll in courses
- Mark attendance via QR codes
- View enrolled courses and sessions

### Lecturer
- View/manage own courses
- View attendance for their courses
- Generate QR codes for sessions
- View student lists for their courses

### Admin
- Full access to all resources
- Manage users, courses, and attendance
- Access all analytics and reports

## Error Responses

### Common HTTP Status Codes
- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": "Error message description",
  "detail": "Additional error details (optional)"
}
```

## Rate Limiting
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

## CORS
CORS is enabled for the following origins:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- Configurable via `CORS_ALLOWED_ORIGINS` environment variable

## Development Server
To start the development server:
```bash
cd sams-project/backend
python manage.py runserver
```
Server will be available at: `http://localhost:8000`
