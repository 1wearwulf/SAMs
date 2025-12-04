import 'dart:convert';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/constants.dart';
import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  // Login user
  static Future<User> login(String email, String password) async {
    try {
      final deviceInfo = await _getDeviceInfo();

      final response = await ApiService.post(
        Constants.loginEndpoint,
        data: {
          'email': email,
          'password': password,
          'device_info': deviceInfo,
        },
      );

      if (response != null && response['user'] != null && response['tokens'] != null) {
        final user = User.fromJson(response['user']);
        await ApiService.saveAuthData(response['tokens'], user);

        // Register device if not already registered
        await _registerDevice(user.id);

        return user;
      } else {
        throw Exception('Invalid response format');
      }
    } catch (e) {
      throw Exception('Login failed: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Register user
  static Future<User> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    required String studentId,
    required String role,
  }) async {
    try {
      final deviceInfo = await _getDeviceInfo();

      final response = await ApiService.post(
        Constants.registerEndpoint,
        data: {
          'email': email,
          'password': password,
          'first_name': firstName,
          'last_name': lastName,
          'student_id': studentId,
          'role': role,
          'device_info': deviceInfo,
        },
      );

      if (response != null && response['user'] != null && response['tokens'] != null) {
        final user = User.fromJson(response['user']);
        await ApiService.saveAuthData(response['tokens'], user);

        // Register device
        await _registerDevice(user.id);

        return user;
      } else {
        throw Exception('Invalid response format');
      }
    } catch (e) {
      throw Exception('Registration failed: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Logout user
  static Future<void> logout() async {
    try {
      await ApiService.logout();
    } catch (e) {
      // Even if logout request fails, clear local data
      await ApiService.logout();
    }
  }

  // Check if user is authenticated
  static Future<bool> isAuthenticated() async {
    return await ApiService.isAuthenticated();
  }

  // Get current user
  static Future<User?> getCurrentUser() async {
    return await ApiService.getCurrentUser();
  }

  // Refresh user profile
  static Future<User> refreshProfile() async {
    try {
      final response = await ApiService.get(Constants.userProfileEndpoint);

      if (response != null) {
        final user = User.fromJson(response);
        await ApiService.updateCurrentUser(user);
        return user;
      } else {
        throw Exception('Failed to refresh profile');
      }
    } catch (e) {
      throw Exception('Failed to refresh profile: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Update user profile
  static Future<User> updateProfile({
    String? firstName,
    String? lastName,
    String? phone,
    String? profilePicture,
  }) async {
    try {
      final updateData = <String, dynamic>{};

      if (firstName != null) updateData['first_name'] = firstName;
      if (lastName != null) updateData['last_name'] = lastName;
      if (phone != null) updateData['phone'] = phone;
      if (profilePicture != null) updateData['profile_picture'] = profilePicture;

      final response = await ApiService.put(
        Constants.userProfileEndpoint,
        data: updateData,
      );

      if (response != null) {
        final user = User.fromJson(response);
        await ApiService.updateCurrentUser(user);
        return user;
      } else {
        throw Exception('Failed to update profile');
      }
    } catch (e) {
      throw Exception('Failed to update profile: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Change password
  static Future<void> changePassword(String currentPassword, String newPassword) async {
    try {
      await ApiService.post(
        '${Constants.userProfileEndpoint}change-password/',
        data: {
          'current_password': currentPassword,
          'new_password': newPassword,
        },
      );
    } catch (e) {
      throw Exception('Failed to change password: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Request password reset
  static Future<void> requestPasswordReset(String email) async {
    try {
      await ApiService.post(
        '/auth/password-reset/',
        data: {'email': email},
      );
    } catch (e) {
      throw Exception('Failed to request password reset: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Reset password with token
  static Future<void> resetPassword(String token, String newPassword) async {
    try {
      await ApiService.post(
        '/auth/password-reset/confirm/',
        data: {
          'token': token,
          'password': newPassword,
        },
      );
    } catch (e) {
      throw Exception('Failed to reset password: ${e.toString().replaceFirst('Exception: ', '')}');
    }
  }

  // Get device information
  static Future<Map<String, dynamic>> _getDeviceInfo() async {
    try {
      final deviceInfo = DeviceInfoPlugin();
      final deviceId = await ApiService.getDeviceId();

      Map<String, dynamic> deviceData = {
        'device_id': deviceId,
        'device_type': 'mobile',
      };

      if (Platform.isAndroid) {
        final androidInfo = await deviceInfo.androidInfo;
        deviceData.addAll({
          'manufacturer': androidInfo.manufacturer,
          'model': androidInfo.model,
          'os': 'android',
          'os_version': androidInfo.version.release,
          'app_version': Constants.appVersion,
        });
      } else if (Platform.isIOS) {
        final iosInfo = await deviceInfo.iosInfo;
        deviceData.addAll({
          'manufacturer': 'Apple',
          'model': iosInfo.model,
          'os': 'ios',
          'os_version': iosInfo.systemVersion,
          'app_version': Constants.appVersion,
        });
      }

      return deviceData;
    } catch (e) {
      return {
        'device_id': await ApiService.getDeviceId(),
        'device_type': 'mobile',
        'manufacturer': 'Unknown',
        'model': 'Unknown',
        'os': Platform.isAndroid ? 'android' : 'ios',
        'os_version': 'Unknown',
        'app_version': Constants.appVersion,
      };
    }
  }

  // Register device with backend
  static Future<void> _registerDevice(int userId) async {
    try {
      final deviceInfo = await _getDeviceInfo();

      await ApiService.post(
        Constants.deviceRegisterEndpoint,
        data: deviceInfo,
      );
    } catch (e) {
      // Device registration failure shouldn't block login
      print('Device registration failed: $e');
    }
  }

  // Validate session
  static Future<bool> validateSession() async {
    try {
      final response = await ApiService.get('/auth/validate-session/');
      return response != null && response['valid'] == true;
    } catch (e) {
      return false;
    }
  }

  // Get authentication status
  static Future<Map<String, dynamic>> getAuthStatus() async {
    final isAuthenticated = await AuthService.isAuthenticated();
    final user = await AuthService.getCurrentUser();

    return {
      'is_authenticated': isAuthenticated,
      'user': user?.toJson(),
    };
  }
}
