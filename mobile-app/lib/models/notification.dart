enum NotificationType {
  announcement,
  reminder,
  alert,
  system,
}

extension NotificationTypeExtension on NotificationType {
  String get displayName {
    switch (this) {
      case NotificationType.announcement:
        return 'Announcement';
      case NotificationType.reminder:
        return 'Reminder';
      case NotificationType.alert:
        return 'Alert';
      case NotificationType.system:
        return 'System';
    }
  }

  String get value {
    switch (this) {
      case NotificationType.announcement:
        return 'announcement';
      case NotificationType.reminder:
        return 'reminder';
      case NotificationType.alert:
        return 'alert';
      case NotificationType.system:
        return 'system';
    }
  }

  static NotificationType fromString(String value) {
    switch (value.toLowerCase()) {
      case 'announcement':
        return NotificationType.announcement;
      case 'reminder':
        return NotificationType.reminder;
      case 'alert':
        return NotificationType.alert;
      case 'system':
        return NotificationType.system;
      default:
        return NotificationType.system;
    }
  }
}

class Notification {
  final int id;
  final String title;
  final String message;
  final NotificationType type;
  final int? senderId;
  final String? senderName;
  final int? courseId;
  final String? courseName;
  final List<int> recipientIds;
  final bool isRead;
  final DateTime? readAt;
  final DateTime sentAt;
  final DateTime createdAt;
  final Map<String, dynamic>? metadata;

  Notification({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    this.senderId,
    this.senderName,
    this.courseId,
    this.courseName,
    required this.recipientIds,
    required this.isRead,
    this.readAt,
    required this.sentAt,
    required this.createdAt,
    this.metadata,
  });

  bool get isAnnouncement => type == NotificationType.announcement;
  bool get isReminder => type == NotificationType.reminder;
  bool get isAlert => type == NotificationType.alert;
  bool get isSystem => type == NotificationType.system;

  String get formattedTime {
    final now = DateTime.now();
    final difference = now.difference(sentAt);

    if (difference.inDays > 0) {
      return '${difference.inDays} day${difference.inDays > 1 ? 's' : ''} ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hour${difference.inHours > 1 ? 's' : ''} ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minute${difference.inMinutes > 1 ? 's' : ''} ago';
    } else {
      return 'Just now';
    }
  }

  factory Notification.fromJson(Map<String, dynamic> json) {
    return Notification(
      id: json['id'],
      title: json['title'] ?? '',
      message: json['message'] ?? '',
      type: NotificationTypeExtension.fromString(json['type'] ?? 'system'),
      senderId: json['sender_id'],
      senderName: json['sender_name'],
      courseId: json['course_id'],
      courseName: json['course_name'],
      recipientIds: List<int>.from(json['recipient_ids'] ?? []),
      isRead: json['is_read'] ?? false,
      readAt: json['read_at'] != null ? DateTime.parse(json['read_at']) : null,
      sentAt: DateTime.parse(json['sent_at'] ?? DateTime.now().toIso8601String()),
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
      metadata: json['metadata'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'message': message,
      'type': type.value,
      'sender_id': senderId,
      'sender_name': senderName,
      'course_id': courseId,
      'course_name': courseName,
      'recipient_ids': recipientIds,
      'is_read': isRead,
      'read_at': readAt?.toIso8601String(),
      'sent_at': sentAt.toIso8601String(),
      'created_at': createdAt.toIso8601String(),
      'metadata': metadata,
    };
  }
}

class PushNotificationToken {
  final int id;
  final int userId;
  final String token;
  final String deviceType;
  final String? deviceName;
  final bool isActive;
  final DateTime createdAt;
  final DateTime updatedAt;
  final DateTime? lastUsedAt;

  PushNotificationToken({
    required this.id,
    required this.userId,
    required this.token,
    required this.deviceType,
    this.deviceName,
    required this.isActive,
    required this.createdAt,
    required this.updatedAt,
    this.lastUsedAt,
  });

  factory PushNotificationToken.fromJson(Map<String, dynamic> json) {
    return PushNotificationToken(
      id: json['id'],
      userId: json['user_id'] ?? 0,
      token: json['token'] ?? '',
      deviceType: json['device_type'] ?? 'unknown',
      deviceName: json['device_name'],
      isActive: json['is_active'] ?? true,
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
      updatedAt: DateTime.parse(json['updated_at'] ?? DateTime.now().toIso8601String()),
      lastUsedAt: json['last_used_at'] != null ? DateTime.parse(json['last_used_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'token': token,
      'device_type': deviceType,
      'device_name': deviceName,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'last_used_at': lastUsedAt?.toIso8601String(),
    };
  }
}

class NotificationPreference {
  final int id;
  final int userId;
  final bool announcements;
  final bool reminders;
  final bool alerts;
  final bool systemNotifications;
  final bool emailNotifications;
  final bool pushNotifications;
  final DateTime createdAt;
  final DateTime updatedAt;

  NotificationPreference({
    required this.id,
    required this.userId,
    required this.announcements,
    required this.reminders,
    required this.alerts,
    required this.systemNotifications,
    required this.emailNotifications,
    required this.pushNotifications,
    required this.createdAt,
    required this.updatedAt,
  });

  factory NotificationPreference.fromJson(Map<String, dynamic> json) {
    return NotificationPreference(
      id: json['id'],
      userId: json['user_id'] ?? 0,
      announcements: json['announcements'] ?? true,
      reminders: json['reminders'] ?? true,
      alerts: json['alerts'] ?? true,
      systemNotifications: json['system_notifications'] ?? true,
      emailNotifications: json['email_notifications'] ?? false,
      pushNotifications: json['push_notifications'] ?? true,
      createdAt: DateTime.parse(json['created_at'] ?? DateTime.now().toIso8601String()),
      updatedAt: DateTime.parse(json['updated_at'] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'announcements': announcements,
      'reminders': reminders,
      'alerts': alerts,
      'system_notifications': systemNotifications,
      'email_notifications': emailNotifications,
      'push_notifications': pushNotifications,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class NotificationStats {
  final int totalNotifications;
  final int unreadCount;
  final int todayCount;
  final int thisWeekCount;
  final Map<String, int> typeBreakdown;

  NotificationStats({
    required this.totalNotifications,
    required this.unreadCount,
    required this.todayCount,
    required this.thisWeekCount,
    required this.typeBreakdown,
  });

  factory NotificationStats.fromJson(Map<String, dynamic> json) {
    return NotificationStats(
      totalNotifications: json['total_notifications'] ?? 0,
      unreadCount: json['unread_count'] ?? 0,
      todayCount: json['today_count'] ?? 0,
      thisWeekCount: json['this_week_count'] ?? 0,
      typeBreakdown: Map<String, int>.from(json['type_breakdown'] ?? {}),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_notifications': totalNotifications,
      'unread_count': unreadCount,
      'today_count': todayCount,
      'this_week_count': thisWeekCount,
      'type_breakdown': typeBreakdown,
    };
  }
}
