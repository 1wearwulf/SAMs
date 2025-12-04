import 'dart:convert';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../core/constants.dart';
import '../models/notification.dart';
import 'api_service.dart';

class NotificationService {
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  static late FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;

  // Initialize Firebase Messaging and Local Notifications
  static Future<void> initialize() async {
    // Request permission for notifications
    await _firebaseMessaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );

    // Get FCM token
    final fcmToken = await _firebaseMessaging.getToken();
    if (fcmToken != null) {
      await _registerTokenWithBackend(fcmToken);
    }

    // Initialize local notifications
    flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();

    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');

    const InitializationSettings initializationSettings =
        InitializationSettings(android: initializationSettingsAndroid);

    await flutterLocalNotificationsPlugin.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: (NotificationResponse response) {
        _handleNotificationTap(response.payload);
      },
    );

    // Handle background messages
    FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

    // Handle notification tap when app is in background
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTapFromBackground);
  }

  // Register FCM token with backend
  static Future<void> _registerTokenWithBackend(String token) async {
    try {
      await ApiService.post(
        '/notifications/register-token/',
        data: {
          'token': token,
          'device_type': 'mobile',
          'device_name': 'Flutter App',
        },
      );
    } catch (e) {
      print('Failed to register FCM token: $e');
    }
  }

  // Handle background messages
  static Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
    print('Handling background message: ${message.messageId}');

    final notification = message.notification;
    final data = message.data;

    if (notification != null) {
      await _showLocalNotification(
        id: message.hashCode,
        title: notification.title ?? 'Notification',
        body: notification.body ?? '',
        payload: jsonEncode(data),
      );
    }
  }

  // Handle foreground messages
  static void _handleForegroundMessage(RemoteMessage message) {
    print('Handling foreground message: ${message.messageId}');

    final notification = message.notification;
    final data = message.data;

    if (notification != null) {
      _showLocalNotification(
        id: message.hashCode,
        title: notification.title ?? 'Notification',
        body: notification.body ?? '',
        payload: jsonEncode(data),
      );
    }
  }

  // Handle notification tap from background
  static void _handleNotificationTapFromBackground(RemoteMessage message) {
    print('Notification tapped from background: ${message.messageId}');
    _handleNotificationTap(jsonEncode(message.data));
  }

  // Handle notification tap
  static void _handleNotificationTap(String? payload) {
    if (payload != null) {
      try {
        final data = jsonDecode(payload) as Map<String, dynamic>;
        // Navigate to appropriate screen based on notification type
        _navigateBasedOnNotification(data);
      } catch (e) {
        print('Error parsing notification payload: $e');
      }
    }
  }

  // Navigate based on notification type
  static void _navigateBasedOnNotification(Map<String, dynamic> data) {
    final type = data['type'];
    final courseId = data['course_id'];
    final sessionId = data['session_id'];

    // This would typically use a navigation service or provider
    // For now, we'll just print the navigation intent
    print('Navigate to: type=$type, courseId=$courseId, sessionId=$sessionId');
  }

  // Show local notification
  static Future<void> _showLocalNotification({
    required int id,
    required String title,
    required String body,
    String? payload,
  }) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      Constants.attendanceChannelId,
      'Attendance Notifications',
      channelDescription: 'Notifications for attendance updates',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: true,
      enableVibration: true,
      playSound: true,
    );

    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);

    await flutterLocalNotificationsPlugin.show(
      id,
      title,
      body,
      platformChannelSpecifics,
      payload: payload,
    );
  }

  // Get notifications from backend
  static Future<List<Notification>> getNotifications({
    int page = 1,
    int limit = 20,
    bool unreadOnly = false,
  }) async {
    try {
      final queryParams = <String, dynamic>{
        'page': page.toString(),
        'limit': limit.toString(),
      };

      if (unreadOnly) queryParams['unread_only'] = 'true';

      final response = await ApiService.get(
        Constants.notificationsEndpoint,
        queryParams: queryParams,
      );

      if (response != null && response['results'] != null) {
        final List<dynamic> results = response['results'];
        return results.map((item) => Notification.fromJson(item)).toList();
      } else {
        return [];
      }
    } catch (e) {
      throw Exception('Failed to get notifications: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Mark notification as read
  static Future<void> markAsRead(int notificationId) async {
    try {
      await ApiService.post(
        '${Constants.notificationsEndpoint}$notificationId/mark-read/',
      );
    } catch (e) {
      throw Exception('Failed to mark notification as read: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Mark all notifications as read
  static Future<void> markAllAsRead() async {
    try {
      await ApiService.post('${Constants.notificationsEndpoint}mark-all-read/');
    } catch (e) {
      throw Exception('Failed to mark all notifications as read: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Get unread count
  static Future<int> getUnreadCount() async {
    try {
      final response = await ApiService.get('${Constants.notificationsEndpoint}unread-count/');

      if (response != null && response['unread_count'] != null) {
        return response['unread_count'] as int;
      } else {
        return 0;
      }
    } catch (e) {
      return 0;
    }
  }

  // Delete notification
  static Future<void> deleteNotification(int notificationId) async {
    try {
      await ApiService.delete('${Constants.notificationsEndpoint}$notificationId/');
    } catch (e) {
      throw Exception('Failed to delete notification: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Get notification preferences
  static Future<NotificationPreference> getNotificationPreferences() async {
    try {
      final response = await ApiService.get('${Constants.notificationsEndpoint}preferences/');

      if (response != null) {
        return NotificationPreference.fromJson(response);
      } else {
        throw Exception('Failed to get notification preferences');
      }
    } catch (e) {
      throw Exception('Failed to get notification preferences: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Update notification preferences
  static Future<NotificationPreference> updateNotificationPreferences({
    bool? announcements,
    bool? reminders,
    bool? alerts,
    bool? systemNotifications,
    bool? emailNotifications,
    bool? pushNotifications,
  }) async {
    try {
      final updateData = <String, dynamic>{};

      if (announcements != null) updateData['announcements'] = announcements;
      if (reminders != null) updateData['reminders'] = reminders;
      if (alerts != null) updateData['alerts'] = alerts;
      if (systemNotifications != null) updateData['system_notifications'] = systemNotifications;
      if (emailNotifications != null) updateData['email_notifications'] = emailNotifications;
      if (pushNotifications != null) updateData['push_notifications'] = pushNotifications;

      final response = await ApiService.put(
        '${Constants.notificationsEndpoint}preferences/',
        data: updateData,
      );

      if (response != null) {
        return NotificationPreference.fromJson(response);
      } else {
        throw Exception('Failed to update notification preferences');
      }
    } catch (e) {
      throw Exception('Failed to update notification preferences: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Get notification statistics
  static Future<NotificationStats> getNotificationStats() async {
    try {
      final response = await ApiService.get('${Constants.notificationsEndpoint}stats/');

      if (response != null) {
        return NotificationStats.fromJson(response);
      } else {
        throw Exception('Failed to get notification stats');
      }
    } catch (e) {
      throw Exception('Failed to get notification stats: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Send test notification (for development)
  static Future<void> sendTestNotification() async {
    try {
      await ApiService.post(
        '${Constants.notificationsEndpoint}test/',
        data: {
          'title': 'Test Notification',
          'message': 'This is a test notification from the app',
        },
      );
    } catch (e) {
      throw Exception('Failed to send test notification: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Clear all notifications
  static Future<void> clearAllNotifications() async {
    try {
      await flutterLocalNotificationsPlugin.cancelAll();
    } catch (e) {
      print('Failed to clear local notifications: $e');
    }
  }

  // Schedule reminder notification
  static Future<void> scheduleReminder({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledTime,
    String? payload,
  }) async {
    try {
      const AndroidNotificationDetails androidPlatformChannelSpecifics =
          AndroidNotificationDetails(
        Constants.reminderChannelId,
        'Reminders',
        channelDescription: 'Scheduled reminders',
        importance: Importance.max,
        priority: Priority.high,
        showWhen: true,
        enableVibration: true,
        playSound: true,
      );

      const NotificationDetails platformChannelSpecifics =
          NotificationDetails(android: androidPlatformChannelSpecifics);

      await flutterLocalNotificationsPlugin.schedule(
        id,
        title,
        body,
        scheduledTime,
        platformChannelSpecifics,
        payload: payload,
        androidAllowWhileIdle: true,
      );
    } catch (e) {
      print('Failed to schedule reminder: $e');
    }
  }

  // Cancel scheduled notification
  static Future<void> cancelScheduledNotification(int id) async {
    try {
      await flutterLocalNotificationsPlugin.cancel(id);
    } catch (e) {
      print('Failed to cancel scheduled notification: $e');
    }
  }
}
