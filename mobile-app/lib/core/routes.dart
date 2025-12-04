import 'package:flutter/material.dart';
import '../ui/screens/splash_screen.dart';
import '../ui/screens/login_screen.dart';
import '../ui/screens/home_screen.dart';
import '../ui/screens/scan_qr_screen.dart';
import '../ui/screens/notifications_screen.dart';
import '../ui/screens/profile_screen.dart';
import '../ui/screens/attendance_history_screen.dart';
import '../ui/screens/course_details_screen.dart';

class Routes {
  // Route names
  static const String splash = '/';
  static const String login = '/login';
  static const String home = '/home';
  static const String scanQr = '/scan-qr';
  static const String notifications = '/notifications';
  static const String profile = '/profile';
  static const String attendanceHistory = '/attendance-history';
  static const String courseDetails = '/course-details';

  // Route map
  static Map<String, WidgetBuilder> get routes => {
        splash: (context) => const SplashScreen(),
        login: (context) => const LoginScreen(),
        home: (context) => const HomeScreen(),
        scanQr: (context) => const ScanQrScreen(),
        notifications: (context) => const NotificationsScreen(),
        profile: (context) => const ProfileScreen(),
        attendanceHistory: (context) => const AttendanceHistoryScreen(),
        courseDetails: (context) => const CourseDetailsScreen(),
      };

  // Navigation helpers
  static void navigateTo(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushNamed(context, routeName, arguments: arguments);
  }

  static void navigateAndReplace(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushReplacementNamed(context, routeName, arguments: arguments);
  }

  static void navigateAndRemoveUntil(BuildContext context, String routeName, {Object? arguments}) {
    Navigator.pushNamedAndRemoveUntil(
      context,
      routeName,
      (route) => false,
      arguments: arguments,
    );
  }

  static void goBack(BuildContext context) {
    Navigator.pop(context);
  }

  static void goBackWithResult(BuildContext context, dynamic result) {
    Navigator.pop(context, result);
  }
}
