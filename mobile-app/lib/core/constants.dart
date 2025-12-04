class Constants {
  // API Configuration
  static const String baseUrl = 'http://10.0.2.2:8000/api'; // Android emulator
  // static const String baseUrl = 'http://localhost:8000/api'; // iOS simulator
  // static const String baseUrl = 'https://your-production-api.com/api'; // Production

  // API Endpoints
  static const String loginEndpoint = '/auth/login/';
  static const String registerEndpoint = '/auth/register/';
  static const String refreshTokenEndpoint = '/auth/token/refresh/';
  static const String userProfileEndpoint = '/accounts/profile/';
  static const String coursesEndpoint = '/courses/';
  static const String attendanceEndpoint = '/attendance/';
  static const String qrScanEndpoint = '/attendance/scan/';
  static const String notificationsEndpoint = '/notifications/';
  static const String deviceRegisterEndpoint = '/devices/register/';

  // Storage Keys
  static const String accessTokenKey = 'access_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String userDataKey = 'user_data';
  static const String deviceIdKey = 'device_id';
  static const String themeModeKey = 'theme_mode';
  static const String notificationSettingsKey = 'notification_settings';

  // Location Settings
  static const double defaultGeofenceRadius = 100.0; // meters
  static const int locationUpdateInterval = 5000; // milliseconds
  static const double locationAccuracyThreshold = 50.0; // meters

  // QR Code Settings
  static const int qrScanTimeout = 30; // seconds
  static const int qrValidityPeriod = 90; // seconds

  // App Settings
  static const String appName = 'Smart Attendance System';
  static const String appVersion = '1.0.0';
  static const int sessionTimeoutMinutes = 60;

  // Error Messages
  static const String networkError = 'Network connection failed. Please check your internet connection.';
  static const String locationPermissionDenied = 'Location permission is required for attendance marking.';
  static const String cameraPermissionDenied = 'Camera permission is required for QR code scanning.';
  static const String invalidQRError = 'Invalid or expired QR code. Please try again.';
  static const String locationOutOfRangeError = 'You are outside the allowed location for this session.';
  static const String sessionExpiredError = 'Your session has expired. Please login again.';
  static const String deviceNotRegisteredError = 'This device is not registered for attendance marking.';

  // Success Messages
  static const String attendanceMarkedSuccess = 'Attendance marked successfully!';
  static const String loginSuccess = 'Login successful!';
  static const String logoutSuccess = 'Logged out successfully!';

  // Validation Messages
  static const String emailRequired = 'Email is required';
  static const String passwordRequired = 'Password is required';
  static const String passwordTooShort = 'Password must be at least 8 characters';
  static const String invalidEmail = 'Please enter a valid email address';

  // Animation Durations
  static const Duration shortAnimationDuration = Duration(milliseconds: 200);
  static const Duration mediumAnimationDuration = Duration(milliseconds: 500);
  static const Duration longAnimationDuration = Duration(milliseconds: 1000);

  // UI Constants
  static const double defaultPadding = 16.0;
  static const double defaultBorderRadius = 12.0;
  static const double defaultElevation = 4.0;
  static const double cardBorderRadius = 16.0;
  static const double buttonBorderRadius = 25.0;

  // Colors
  static const int primaryColorValue = 0xFF1976D2;
  static const int secondaryColorValue = 0xFFDC143C;
  static const int successColorValue = 0xFF4CAF50;
  static const int errorColorValue = 0xFFF44336;
  static const int warningColorValue = 0xFFFF9800;

  // Notification Channels
  static const String attendanceChannelId = 'attendance_channel';
  static const String generalChannelId = 'general_channel';
  static const String reminderChannelId = 'reminder_channel';

  // Cache Settings
  static const Duration cacheTimeout = Duration(hours: 1);
  static const int maxCacheSize = 100;

  // Retry Settings
  static const int maxRetryAttempts = 3;
  static const Duration retryDelay = Duration(seconds: 2);
}
