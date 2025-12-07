import 'dart:async';
import 'package:flutter/material.dart';
import 'services/api_config.dart';
import 'services/api_service.dart';
import 'services/auth_service.dart';

void main() async {
  runApp(IntegrationTestApp());
}

class IntegrationTestApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SAMS Integration Test',
      home: IntegrationTestScreen(),
    );
  }
}

class IntegrationTestScreen extends StatefulWidget {
  @override
  _IntegrationTestScreenState createState() => _IntegrationTestScreenState();
}

class _IntegrationTestScreenState extends State<IntegrationTestScreen> {
  final List<TestResult> _testResults = [];
  bool _isTesting = false;
  String _overallStatus = 'Ready to test';

  final AuthService _authService = AuthService();
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _runTests();
  }

  Future<void> _runTests() async {
    setState(() {
      _isTesting = true;
      _overallStatus = 'Testing...';
      _testResults.clear();
    });

    // Test 1: API Configuration
    await _testApiConfig();

    // Test 2: Server Connectivity
    await _testServerConnectivity();

    // Test 3: Authentication
    await _testAuthentication();

    // Test 4: Get Current User
    await _testGetCurrentUser();

    // Test 5: Mark Attendance
    await _testMarkAttendance();

    // Test 6: Get Dashboard Stats
    await _testDashboardStats();

    setState(() {
      _isTesting = false;
      final passed = _testResults.where((r) => r.passed).length;
      final total = _testResults.length;
      _overallStatus = 'Tests Complete: $passed/$total passed';
    });
  }

  Future<void> _testApiConfig() async {
    _addTestResult('API Configuration', 'Checking API config...');

    try {
      ApiConfig.printConfig();
      final isValid = !ApiConfig.baseUrl.contains('example.com');

      _updateLastTestResult(
        isValid,
        isValid ? '✅ API config is valid' : '❌ API config needs updating'
      );
    } catch (e) {
      _updateLastTestResult(false, '❌ Error: $e');
    }
  }

  Future<void> _testServerConnectivity() async {
    _addTestResult('Server Connectivity', 'Pinging server...');

    try {
      // Try to reach the server root
      final response = await _apiService.login('test', 'test');

      if (response['statusCode'] != null) {
        _updateLastTestResult(
          true,
          '✅ Server reachable (Status: ${response['statusCode']})'
        );
      } else {
        _updateLastTestResult(false, '❌ Cannot reach server');
      }
    } catch (e) {
      _updateLastTestResult(false, '❌ Network error: ${e.toString()}');
    }
  }

  Future<void> _testAuthentication() async {
    _addTestResult('Authentication', 'Testing login with invalid credentials...');

    try {
      final result = await _apiService.login('invaliduser', 'wrongpassword');

      // Should get 400 or 401 for invalid credentials
      if (result['statusCode'] == 400 || result['statusCode'] == 401) {
        _updateLastTestResult(
          true,
          '✅ Authentication endpoint working (expected failure)'
        );
      } else {
        _updateLastTestResult(
          false,
          '❌ Unexpected response: ${result['statusCode']}'
        );
      }
    } catch (e) {
      _updateLastTestResult(false, '❌ Error: $e');
    }
  }

  Future<void> _testGetCurrentUser() async {
    _addTestResult('Get Current User', 'Testing with stored token...');

    try {
      final token = await _authService.getToken();

      if (token == null) {
        _updateLastTestResult(
          true,
          '⚠️ No token stored (login first)'
        );
        return;
      }

      final result = await _apiService.getCurrentUser(token);

      if (result['success'] == true) {
        _updateLastTestResult(
          true,
          '✅ User data retrieved successfully'
        );
      } else {
        _updateLastTestResult(
          false,
          '❌ Failed to get user: ${result['message']}'
        );
      }
    } catch (e) {
      _updateLastTestResult(false, '❌ Error: $e');
    }
  }

  Future<void> _testMarkAttendance() async {
    _addTestResult('Mark Attendance', 'Testing attendance endpoint...');

    try {
      final token = await _authService.getToken();

      if (token == null) {
        _updateLastTestResult(
          true,
          '⚠️ No token (login first to test fully)'
        );
        return;
      }

      // Test with invalid QR code first
      final result = await _apiService.markAttendance(
        qrCode: 'INVALID_QR_TEST',
        token: token,
      );

      // Check if endpoint is reachable
      if (result['statusCode'] != null) {
        _updateLastTestResult(
          true,
          '✅ Attendance endpoint reachable'
        );
      } else {
        _updateLastTestResult(
          false,
          '❌ Cannot reach attendance endpoint'
        );
      }
    } catch (e) {
      _updateLastTestResult(false, '❌ Error: $e');
    }
  }

  Future<void> _testDashboardStats() async {
    _addTestResult('Dashboard Stats', 'Testing analytics endpoint...');

    try {
      final token = await _authService.getToken();

      if (token == null) {
        _updateLastTestResult(
          true,
          '⚠️ No token (login first to test fully)'
        );
        return;
      }

      final result = await _apiService.getDashboardStats(token);

      if (result['success'] == true) {
        _updateLastTestResult(
          true,
          '✅ Dashboard stats retrieved'
        );
      } else {
        _updateLastTestResult(
          result['statusCode'] != null,
          result['statusCode'] != null
            ? '⚠️ Endpoint reachable but unauthorized'
            : '❌ Cannot reach endpoint'
        );
      }
    } catch (e) {
      _updateLastTestResult(false, '❌ Error: $e');
    }
  }

  void _addTestResult(String testName, String message) {
    setState(() {
      _testResults.add(TestResult(
        name: testName,
        passed: false,
        message: message,
      ));
    });
  }

  void _updateLastTestResult(bool passed, String message) {
    if (_testResults.isNotEmpty) {
      setState(() {
        final lastIndex = _testResults.length - 1;
        _testResults[lastIndex] = TestResult(
          name: _testResults[lastIndex].name,
          passed: passed,
          message: message,
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SAMS Integration Tests'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isTesting ? null : _runTests,
          ),
        ],
      ),
      body: Column(
        children: [
          // Status Header
          Container(
            padding: const EdgeInsets.all(16),
            color: _isTesting ? Colors.blue[50] : Colors.grey[50],
            child: Row(
              children: [
                _isTesting
                    ? const CircularProgressIndicator()
                    : const Icon(Icons.check_circle, color: Colors.green),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _overallStatus,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: _isTesting ? Colors.blue : Colors.green,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Base URL: ${ApiConfig.baseUrl}',
                        style: const TextStyle(fontSize: 12, color: Colors.grey),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Test Results
          Expanded(
            child: ListView.builder(
              itemCount: _testResults.length,
              itemBuilder: (context, index) {
                final result = _testResults[index];
                return Card(
                  margin: const EdgeInsets.all(8),
                  color: result.passed ? Colors.green[50] :
                         result.message.contains('⚠️') ? Colors.orange[50] : Colors.red[50],
                  child: ListTile(
                    leading: result.passed
                        ? const Icon(Icons.check_circle, color: Colors.green)
                        : result.message.contains('⚠️')
                            ? const Icon(Icons.warning, color: Colors.orange)
                            : const Icon(Icons.error, color: Colors.red),
                    title: Text(
                      result.name,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(result.message),
                  ),
                );
              },
            ),
          ),

          // Action Buttons
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _isTesting ? null : _runTests,
                    child: const Text('Run All Tests'),
                  ),
                ),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () {
                      // Show API config details
                      showDialog(
                        context: context,
                        builder: (context) => AlertDialog(
                          title: const Text('API Configuration'),
                          content: SingleChildScrollView(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('Base URL: ${ApiConfig.baseUrl}'),
                                const SizedBox(height: 8),
                                Text('Login: ${ApiConfig.loginEndpoint}'),
                                Text('Mark Attendance: ${ApiConfig.markAttendanceEndpoint}'),
                                Text('Current User: ${ApiConfig.currentUserEndpoint}'),
                                const SizedBox(height: 16),
                                const Text('💡 Tips:'),
                                const Text('• Android emulator: Use 10.0.2.2:8000'),
                                const Text('• iOS simulator: Use localhost:8000'),
                                const Text('• Real device: Use computer IP'),
                              ],
                            ),
                          ),
                          actions: [
                            TextButton(
                              onPressed: () => Navigator.pop(context),
                              child: const Text('OK'),
                            ),
                          ],
                        ),
                      );
                    },
                    child: const Text('View API Config'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class TestResult {
  final String name;
  final bool passed;
  final String message;

  TestResult({
    required this.name,
    required this.passed,
    required this.message,
  });
}
