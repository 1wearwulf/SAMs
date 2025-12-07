import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'api_config.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.loginEndpoint}'),
        headers: ApiConfig.getHeaders(null),
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }

  Future<Map<String, dynamic>> markAttendance({
    required String qrCode,
    required String token,
    double? latitude,
    double? longitude,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.markAttendanceEndpoint}'),
        headers: ApiConfig.getHeaders(token),
        body: jsonEncode({
          'qr_code': qrCode,
          if (latitude != null) 'latitude': latitude,
          if (longitude != null) 'longitude': longitude,
          'device_fingerprint': 'flutter_mobile_${DateTime.now().millisecondsSinceEpoch}',
        }),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getCurrentUser(String token) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.currentUserEndpoint}'),
        headers: ApiConfig.getHeaders(token),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getAttendanceHistory(String token) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.attendanceEndpoint}'),
        headers: ApiConfig.getHeaders(token),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }

  Future<Map<String, dynamic>> verifyQR(String qrCode, String token) async {
    try {
      final response = await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.verifyQREndpoint}'),
        headers: ApiConfig.getHeaders(token),
        body: jsonEncode({
          'code': qrCode,
        }),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      return _handleError(e);
    }
  }

  Map<String, dynamic> _handleResponse(http.Response response) {
    final statusCode = response.statusCode;
    final body = response.body.isNotEmpty ? jsonDecode(response.body) : {};

    return {
      'success': statusCode >= 200 && statusCode < 300,
      'statusCode': statusCode,
      'data': body,
      'message': body['message'] ?? body['detail'] ?? (statusCode == 200 ? 'Success' : 'Request failed'),
    };
  }

  Map<String, dynamic> _handleError(dynamic error) {
    return {
      'success': false,
      'error': error.toString(),
      'message': error is SocketException
          ? 'Network error. Check your connection.'
          : 'An error occurred. Please try again.',
    };
  }
}
