enum AttendanceStatus {
  present,
  absent,
  late,
  excused,
}

extension AttendanceStatusExtension on AttendanceStatus {
  String get displayName {
    switch (this) {
      case AttendanceStatus.present:
        return 'Present';
      case AttendanceStatus.absent:
        return 'Absent';
      case AttendanceStatus.late:
        return 'Late';
      case AttendanceStatus.excused:
        return 'Excused';
    }
  }

  String get value {
    switch (this) {
      case AttendanceStatus.present:
        return 'present';
      case AttendanceStatus.absent:
        return 'absent';
      case AttendanceStatus.late:
        return 'late';
      case AttendanceStatus.excused:
        return 'excused';
    }
  }

  static AttendanceStatus fromString(String value) {
    switch (value.toLowerCase()) {
      case 'present':
        return AttendanceStatus.present;
      case 'absent':
        return AttendanceStatus.absent;
      case 'late':
        return AttendanceStatus.late;
      case 'excused':
        return AttendanceStatus.excused;
      default:
        return AttendanceStatus.absent;
    }
  }
}

class Attendance {
  final int id;
  final int studentId;
  final int sessionId;
  final AttendanceStatus status;
  final DateTime timestamp;
  final double? latitude;
  final double? longitude;
  final String? deviceId;
  final String? notes;
  final bool isValid;
  final String? validationErrors;
  final DateTime createdAt;
  final DateTime updatedAt;

  Attendance({
    required this.id,
    required this.studentId,
    required this.sessionId,
    required this.status,
    required this.timestamp,
    this.latitude,
    this.longitude,
    this.deviceId,
    this.notes,
    required this.isValid,
    this.validationErrors,
    required this.createdAt,
    required this.updatedAt,
  });

  bool get isLate => status == AttendanceStatus.late;
  bool get isPresent => status == AttendanceStatus.present;
  bool get isAbsent => status == AttendanceStatus.absent;
  bool get isExcused => status == AttendanceStatus.excused;

  factory Attendance.fromJson(Map<String, dynamic> json) {
    return Attendance(
      id: json['id'],
      studentId: json['student_id'],
      sessionId: json['session_id'],
      status: AttendanceStatusExtension.fromString(json['status']),
      timestamp: DateTime.parse(json['timestamp']),
      latitude: json['latitude']?.toDouble(),
      longitude: json['longitude']?.toDouble(),
      deviceId: json['device_id'],
      notes: json['notes'],
      isValid: json['is_valid'] ?? true,
      validationErrors: json['validation_errors'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'student_id': studentId,
      'session_id': sessionId,
      'status': status.value,
      'timestamp': timestamp.toIso8601String(),
      'latitude': latitude,
      'longitude': longitude,
      'device_id': deviceId,
      'notes': notes,
      'is_valid': isValid,
      'validation_errors': validationErrors,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

class AttendanceSummary {
  final int totalSessions;
  final int presentCount;
  final int absentCount;
  final int lateCount;
  final int excusedCount;
  final double attendanceRate;
  final DateTime? lastAttendanceDate;

  AttendanceSummary({
    required this.totalSessions,
    required this.presentCount,
    required this.absentCount,
    required this.lateCount,
    required this.excusedCount,
    required this.attendanceRate,
    this.lastAttendanceDate,
  });

  factory AttendanceSummary.fromJson(Map<String, dynamic> json) {
    return AttendanceSummary(
      totalSessions: json['total_sessions'] ?? 0,
      presentCount: json['present_count'] ?? 0,
      absentCount: json['absent_count'] ?? 0,
      lateCount: json['late_count'] ?? 0,
      excusedCount: json['excused_count'] ?? 0,
      attendanceRate: (json['attendance_rate'] ?? 0).toDouble(),
      lastAttendanceDate: json['last_attendance_date'] != null
          ? DateTime.parse(json['last_attendance_date'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_sessions': totalSessions,
      'present_count': presentCount,
      'absent_count': absentCount,
      'late_count': lateCount,
      'excused_count': excusedCount,
      'attendance_rate': attendanceRate,
      'last_attendance_date': lastAttendanceDate?.toIso8601String(),
    };
  }
}

class AttendanceRecord {
  final Attendance attendance;
  final String courseName;
  final String courseCode;
  final String sessionTitle;
  final DateTime sessionDate;
  final String lecturerName;

  AttendanceRecord({
    required this.attendance,
    required this.courseName,
    required this.courseCode,
    required this.sessionTitle,
    required this.sessionDate,
    required this.lecturerName,
  });

  factory AttendanceRecord.fromJson(Map<String, dynamic> json) {
    return AttendanceRecord(
      attendance: Attendance.fromJson(json['attendance']),
      courseName: json['course_name'] ?? '',
      courseCode: json['course_code'] ?? '',
      sessionTitle: json['session_title'] ?? '',
      sessionDate: DateTime.parse(json['session_date']),
      lecturerName: json['lecturer_name'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'attendance': attendance.toJson(),
      'course_name': courseName,
      'course_code': courseCode,
      'session_title': sessionTitle,
      'session_date': sessionDate.toIso8601String(),
      'lecturer_name': lecturerName,
    };
  }
}
