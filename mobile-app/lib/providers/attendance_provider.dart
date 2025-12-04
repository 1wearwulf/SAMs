import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';
import '../models/attendance.dart';
import '../models/course.dart';
import '../services/attendance_service.dart';

class AttendanceProvider with ChangeNotifier {
  List<AttendanceRecord> _attendanceHistory = [];
  AttendanceSummary? _attendanceSummary;
  bool _isLoading = false;
  String? _error;
  Position? _currentPosition;

  List<AttendanceRecord> get attendanceHistory => _attendanceHistory;
  AttendanceSummary? get attendanceSummary => _attendanceSummary;
  bool get isLoading => _isLoading;
  String? get error => _error;
  Position? get currentPosition => _currentPosition;

  // Mark attendance
  Future<bool> markAttendance({
    required String qrCode,
    String? notes,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // Get current location
      _currentPosition = await AttendanceService.getCurrentLocation();

      final attendance = await AttendanceService.markAttendance(
        qrCode: qrCode,
        latitude: _currentPosition!.latitude,
        longitude: _currentPosition!.longitude,
        notes: notes,
      );

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Get attendance history
  Future<bool> getAttendanceHistory({
    int? courseId,
    DateTime? startDate,
    DateTime? endDate,
    int page = 1,
    int limit = 20,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final history = await AttendanceService.getAttendanceHistory(
        courseId: courseId,
        startDate: startDate,
        endDate: endDate,
        page: page,
        limit: limit,
      );

      if (page == 1) {
        _attendanceHistory = history;
      } else {
        _attendanceHistory.addAll(history);
      }

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Get attendance summary
  Future<bool> getAttendanceSummary({int? courseId}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _attendanceSummary = await AttendanceService.getAttendanceSummary(courseId: courseId);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Validate QR code
  Future<Map<String, dynamic>?> validateQRCode(String qrCode) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await AttendanceService.validateQRCode(qrCode);
      _isLoading = false;
      notifyListeners();
      return result;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  // Check geofence
  Future<Map<String, dynamic>?> checkGeofence({
    required double sessionLatitude,
    required double sessionLongitude,
    required double radius,
  }) async {
    try {
      // Get current location
      _currentPosition = await AttendanceService.getCurrentLocation();

      return await AttendanceService.checkGeofence(
        userLatitude: _currentPosition!.latitude,
        userLongitude: _currentPosition!.longitude,
        sessionLatitude: sessionLatitude,
        sessionLongitude: sessionLongitude,
        radius: radius,
      );
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
      return null;
    }
  }

  // Get attendance stats
  Future<Map<String, dynamic>?> getAttendanceStats({int? courseId}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final stats = await AttendanceService.getAttendanceStats(courseId: courseId);
      _isLoading = false;
      notifyListeners();
      return stats;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  // Get current location
  Future<bool> getCurrentLocation() async {
    try {
      _currentPosition = await AttendanceService.getCurrentLocation();
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().replaceFirst('Exception: ', '');
      notifyListeners();
      return false;
    }
  }

  // Clear attendance history
  void clearAttendanceHistory() {
    _attendanceHistory.clear();
    notifyListeners();
  }

  // Clear error
  void clearError() {
    _error = null;
    notifyListeners();
  }

  // Refresh data
  Future<void> refreshData({int? courseId}) async {
    await Future.wait([
      getAttendanceHistory(courseId: courseId),
      getAttendanceSummary(courseId: courseId),
    ]);
  }

  // Get attendance rate for a course
  double getAttendanceRateForCourse(int courseId) {
    final courseRecords = _attendanceHistory.where((record) => record.attendance.sessionId == courseId).toList();
    if (courseRecords.isEmpty) return 0.0;

    final presentCount = courseRecords.where((record) => record.attendance.isPresent).length;
    return (presentCount / courseRecords.length) * 100;
  }

  // Get recent attendance records
  List<AttendanceRecord> getRecentAttendance({int limit = 10}) {
    final sortedRecords = List<AttendanceRecord>.from(_attendanceHistory)
      ..sort((a, b) => b.attendance.timestamp.compareTo(a.attendance.timestamp));

    return sortedRecords.take(limit).toList();
  }

  // Get attendance by status
  Map<AttendanceStatus, int> getAttendanceByStatus() {
    final statusCount = <AttendanceStatus, int>{};

    for (final record in _attendanceHistory) {
      final status = record.attendance.status;
      statusCount[status] = (statusCount[status] ?? 0) + 1;
    }

    return statusCount;
  }

  // Get attendance trend (last 7 days)
  List<Map<String, dynamic>> getAttendanceTrend() {
    final now = DateTime.now();
    final trend = <Map<String, dynamic>>[];

    for (int i = 6; i >= 0; i--) {
      final date = now.subtract(Duration(days: i));
      final dayRecords = _attendanceHistory.where((record) {
        final recordDate = record.attendance.timestamp;
        return recordDate.year == date.year &&
               recordDate.month == date.month &&
               recordDate.day == date.day;
      }).toList();

      final presentCount = dayRecords.where((record) => record.attendance.isPresent).length;
      final totalCount = dayRecords.length;

      trend.add({
        'date': date,
        'present': presentCount,
        'total': totalCount,
        'rate': totalCount > 0 ? (presentCount / totalCount) * 100 : 0.0,
      });
    }

    return trend;
  }

  // Check if attendance is already marked for session
  bool isAttendanceMarked(int sessionId) {
    return _attendanceHistory.any((record) => record.attendance.sessionId == sessionId);
  }

  // Get attendance record for session
  AttendanceRecord? getAttendanceForSession(int sessionId) {
    try {
      return _attendanceHistory.firstWhere((record) => record.attendance.sessionId == sessionId);
    } catch (e) {
      return null;
    }
  }
}
