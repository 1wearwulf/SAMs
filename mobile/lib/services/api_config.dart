class ApiConfig {
  // Base URL for your SAMS backend
  static const String baseUrl = 'http://10.0.2.2:8000/api';  // Use 10.0.2.2 for Android emulator
  // static const String baseUrl = 'http://localhost:8000/api';  // For iOS simulator

  // Authentication
  static const String loginEndpoint = '/auth/login/';
  static const String registerEndpoint = '/auth/register/';
  static const String refreshTokenEndpoint = '/auth/refresh/';

  // User Management
  static const String currentUserEndpoint = '/users/me/';

  // Attendance
  static const String markAttendanceEndpoint = '/attendance/mark/';
  static const String verifyQREndpoint = '/attendance/verify/';
  static const String attendanceEndpoint = '/attendance/';

  // Courses
  static const String coursesEndpoint = '/courses/';

  // Analytics
  static const String dashboardEndpoint = '/analytics/dashboard/';

  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 15);

  // Headers
  static Map<String, String> getHeaders(String? token) {
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
    };
  }
}
