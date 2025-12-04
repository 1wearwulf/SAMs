"""
Constants for the SAMS project.
"""

# Attendance statuses
ATTENDANCE_STATUSES = (
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('excused', 'Excused'),
)

# QR Code expiry (1 hour = 3600 seconds)
QR_CODE_EXPIRY_SECONDS = 3600

# Password reset token expiry (24 hours)
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = 24

# Course statuses
COURSE_STATUSES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('archived', 'Archived'),
    ('draft', 'Draft'),
)

# Session statuses
SESSION_STATUSES = (
    ('scheduled', 'Scheduled'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

# Course types
COURSE_TYPES = (
    ('lecture', 'Lecture'),
    ('lab', 'Laboratory'),
    ('tutorial', 'Tutorial'),
    ('seminar', 'Seminar'),
)

# Enrollment statuses
ENROLLMENT_STATUSES = (
    ('enrolled', 'Enrolled'),
    ('pending', 'Pending'),
    ('dropped', 'Dropped'),
    ('completed', 'Completed'),
)

# User roles
USER_ROLES = (
    ('student', 'Student'),
    ('lecturer', 'Lecturer'),
    ('admin', 'Administrator'),
)

# Notification types
NOTIFICATION_TYPES = (
    ('info', 'Information'),
    ('warning', 'Warning'),
    ('success', 'Success'),
    ('error', 'Error'),
    ('attendance', 'Attendance Update'),
    ('course', 'Course Update'),
)

# Device types
DEVICE_TYPES = (
    ('mobile', 'Mobile'),
    ('tablet', 'Tablet'),
    ('desktop', 'Desktop'),
    ('unknown', 'Unknown'),
)

# Academic years
ACADEMIC_YEARS = (
    ('2023-2024', '2023-2024'),
    ('2024-2025', '2024-2025'),
    ('2025-2026', '2025-2026'),
)

# Semesters
SEMESTERS = (
    ('spring', 'Spring'),
    ('summer', 'Summer'),
    ('fall', 'Fall'),
    ('winter', 'Winter'),
)

# Geofencing and attendance settings
DEFAULT_GEOFENCE_RADIUS_METERS = 100  # Default radius for geofencing (100 meters)
MAX_GEOFENCE_RADIUS_METERS = 500  # Maximum allowed radius for geofencing
GRACE_PERIOD_MINUTES = 5  # Grace period for late attendance (5 minutes)


# OTP expiry (5 minutes = 300 seconds)
OTP_EXPIRY_SECONDS = 300

# Email verification token expiry (24 hours)
EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = 24

# JWT token expiry (24 hours)
JWT_TOKEN_EXPIRY_HOURS = 24

# Refresh token expiry (7 days)
REFRESH_TOKEN_EXPIRY_DAYS = 7