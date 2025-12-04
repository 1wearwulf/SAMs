# SAMS Comprehensive Testing Guide

## Overview
This guide provides thorough testing instructions for the Smart Attendance Management System (SAMS), covering backend API, web dashboard, and mobile app components.

## Prerequisites
- Python 3.8+
- Node.js 16+
- Flutter 3.0+
- Android Studio (for mobile testing)
- PostgreSQL or SQLite

## 1. Backend API Testing

### Setup
```bash
cd sams-project/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### API Endpoints Testing

#### Authentication
```bash
# Register user
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

#### Courses Management
```bash
# Create course
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Computer Science 101","code":"CS101","description":"Intro to CS"}'

# List courses
curl http://localhost:8000/api/courses/
```

#### Attendance Sessions
```bash
# Create attendance session
curl -X POST http://localhost:8000/api/attendance/sessions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course":1,"location":{"lat":40.7128,"lng":-74.0060},"radius":100}'

# Generate QR code
curl http://localhost:8000/api/attendance/qr/1/
```

#### Mark Attendance
```bash
# Mark attendance
curl -X POST http://localhost:8000/api/attendance/mark/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_id":1,"otp":"123456","location":{"lat":40.7128,"lng":-74.0060}}'
```

## 2. Web Dashboard Testing

### Setup
```bash
cd sams-project/web-dashboard
npm install
npm start
```

### Access URLs
- Dashboard: http://localhost:3000
- Login: http://localhost:3000/login

### Testing Scenarios
1. **User Registration/Login**
   - Register new admin user
   - Login with credentials
   - Verify JWT token storage

2. **Dashboard Overview**
   - Check statistics display
   - Verify real-time data updates
   - Test responsive design

3. **Course Management**
   - Create new course
   - Edit existing course
   - Delete course
   - View course details

4. **Student Management**
   - Add new students
   - Bulk import students
   - Edit student profiles
   - View student attendance history

5. **Attendance Sessions**
   - Create new session
   - Generate QR codes
   - Monitor live attendance
   - View session reports

6. **Analytics & Reports**
   - View attendance statistics
   - Generate reports
   - Export data (CSV/PDF)

## 3. Mobile App Testing

### Setup
```bash
cd sams-project/mobile-app
flutter pub get
flutter doctor
```

### Android Testing
```bash
# Run on connected device
flutter run -d android

# Build APK
flutter build apk --debug
```

### iOS Testing (macOS only)
```bash
flutter run -d ios
```

### Testing Scenarios

#### Authentication Flow
1. Launch app
2. Register/Login screen
3. Enter credentials
4. Verify token storage

#### Course Enrollment
1. View available courses
2. Enroll in courses
3. View enrolled courses

#### QR Code Scanning
1. Navigate to scan screen
2. Grant camera permissions
3. Scan QR code
4. Verify attendance marking

#### Attendance History
1. View attendance records
2. Check timestamps
3. View course-wise stats

#### Profile Management
1. View/edit profile
2. Update personal info
3. Change password

#### Notifications
1. Receive push notifications
2. View notification history
3. Mark as read

## 4. End-to-End Testing

### Complete Attendance Flow
1. **Setup Phase**
   - Start backend server
   - Start web dashboard
   - Build/run mobile app

2. **Admin Setup**
   - Login to web dashboard
   - Create courses
   - Add students
   - Create attendance session

3. **Student Flow**
   - Login to mobile app
   - View available courses
   - Scan QR code for attendance
   - Verify attendance marked

4. **Verification**
   - Check web dashboard for attendance
   - Verify real-time updates
   - Check analytics

## 5. Security Testing

### Authentication Security
- Test JWT token expiration
- Verify refresh token functionality
- Test unauthorized access attempts

### Device Security
- Test device fingerprinting
- Verify geofencing restrictions
- Test anti-cheating mechanisms

### API Security
- Test rate limiting
- Verify CORS settings
- Check input validation

## 6. Performance Testing

### Backend Performance
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/courses/
```

### Mobile App Performance
- Test on different devices
- Monitor memory usage
- Check battery consumption

### Web Dashboard Performance
- Test page load times
- Monitor bundle size
- Check Lighthouse scores

## 7. Integration Testing

### API Integration
- Test all CRUD operations
- Verify data consistency
- Check error handling

### Cross-Platform Testing
- Test on multiple Android devices
- Test on multiple browsers
- Verify responsive design

## 8. Troubleshooting

### Common Issues

**Backend Issues:**
- Database connection errors
- Migration failures
- Static file serving

**Frontend Issues:**
- CORS errors
- API connection failures
- Authentication problems

**Mobile Issues:**
- Permission denials
- Build failures
- Emulator connectivity

### Debug Commands
```bash
# Backend debug
python manage.py shell
python manage.py dbshell

# Frontend debug
npm run build
npm run test

# Mobile debug
flutter analyze
flutter test
```

## 9. Test Data

### Sample Users
- Admin: admin@example.com / admin123
- Student: student@example.com / student123

### Sample Courses
- CS101: Computer Science 101
- MATH201: Calculus II
- ENG101: English Literature

## 10. Success Criteria

- [ ] Backend API responds correctly to all endpoints
- [ ] Web dashboard loads and functions properly
- [ ] Mobile app builds and runs on target devices
- [ ] Complete attendance flow works end-to-end
- [ ] Security features function as expected
- [ ] Performance meets acceptable thresholds
- [ ] All major browsers supported
- [ ] Responsive design works on mobile/tablet

## Quick Start Commands

```bash
# Backend
cd backend && python manage.py runserver

# Web Dashboard (new terminal)
cd web-dashboard && npm start

# Mobile App (new terminal)
cd mobile-app && flutter run -d android
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs
3. Verify configuration files
4. Test with sample data
