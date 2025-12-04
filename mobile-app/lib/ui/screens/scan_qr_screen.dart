import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import '../../core/constants.dart';
import '../../core/routes.dart';
import '../../providers/attendance_provider.dart';
import '../widgets/custom_button.dart';

class ScanQrScreen extends StatefulWidget {
  const ScanQrScreen({super.key});

  @override
  State<ScanQrScreen> createState() => _ScanQrScreenState();
}

class _ScanQrScreenState extends State<ScanQrScreen> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;
  bool _isProcessing = false;
  bool _hasScanned = false;
  String? _scannedCode;

  @override
  void reassemble() {
    super.reassemble();
    if (Platform.isAndroid) {
      controller!.pauseCamera();
    } else if (Platform.isIOS) {
      controller!.resumeCamera();
    }
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) {
      if (!_isProcessing && !_hasScanned && scanData.code != null) {
        _processScannedCode(scanData.code!);
      }
    });
  }

  Future<void> _processScannedCode(String code) async {
    setState(() {
      _isProcessing = true;
      _hasScanned = true;
      _scannedCode = code;
    });

    final attendanceProvider = Provider.of<AttendanceProvider>(context, listen: false);

    // Validate QR code first
    final validationResult = await attendanceProvider.validateQRCode(code);

    if (!mounted) return;

    if (validationResult == null) {
      // Invalid QR code
      _showErrorDialog('Invalid QR Code', attendanceProvider.error ?? 'This QR code is not valid for attendance marking.');
      return;
    }

    final sessionData = validationResult['session'];
    final requiresLocation = validationResult['requires_location'] ?? false;

    if (requiresLocation) {
      // Check location permissions and geofencing
      final locationResult = await attendanceProvider.checkGeofence(
        sessionLatitude: sessionData['latitude'],
        sessionLongitude: sessionData['longitude'],
        radius: sessionData['geofence_radius'] ?? Constants.defaultGeofenceRadius,
      );

      if (!mounted) return;

      if (locationResult == null || !locationResult['in_range']) {
        _showErrorDialog(
          'Location Out of Range',
          locationResult?['message'] ?? Constants.locationOutOfRangeError,
        );
        return;
      }
    }

    // Show confirmation dialog
    final confirmed = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('Confirm Attendance'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Course: ${sessionData['course_name']}'),
            Text('Session: ${sessionData['title']}'),
            Text('Lecturer: ${sessionData['lecturer_name']}'),
            const SizedBox(height: 16),
            const Text('Do you want to mark your attendance?'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Mark Attendance'),
          ),
        ],
      ),
    );

    if (confirmed == true && mounted) {
      // Mark attendance
      final success = await attendanceProvider.markAttendance(qrCode: code);

      if (mounted) {
        if (success) {
          _showSuccessDialog();
        } else {
          _showErrorDialog('Attendance Failed', attendanceProvider.error ?? 'Failed to mark attendance. Please try again.');
        }
      }
    } else {
      // Reset scanning state
      setState(() {
        _isProcessing = false;
        _hasScanned = false;
        _scannedCode = null;
      });
    }
  }

  void _showErrorDialog(String title, String message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // Reset scanning state
              setState(() {
                _isProcessing = false;
                _hasScanned = false;
                _scannedCode = null;
              });
            },
            child: const Text('Try Again'),
          ),
        ],
      ),
    );
  }

  void _showSuccessDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        title: const Text('Success!'),
        content: const Text('Your attendance has been marked successfully.'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Routes.navigateAndReplace(context, Routes.home);
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan QR Code'),
        actions: [
          IconButton(
            icon: const Icon(Icons.flash_on),
            onPressed: () async {
              await controller?.toggleFlash();
            },
          ),
          IconButton(
            icon: const Icon(Icons.flip_camera_android),
            onPressed: () async {
              await controller?.flipCamera();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            flex: 5,
            child: QRView(
              key: qrKey,
              onQRViewCreated: _onQRViewCreated,
              overlay: QrScannerOverlayShape(
                borderColor: Theme.of(context).primaryColor,
                borderRadius: 10,
                borderLength: 30,
                borderWidth: 10,
                cutOutSize: MediaQuery.of(context).size.width * 0.8,
              ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Container(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (_isProcessing)
                    const Column(
                      children: [
                        CircularProgressIndicator(),
                        SizedBox(height: 16),
                        Text(
                          'Processing...',
                          style: TextStyle(fontSize: 16),
                        ),
                      ],
                    )
                  else if (_hasScanned)
                    Column(
                      children: [
                        Icon(
                          Icons.check_circle,
                          color: Colors.green,
                          size: 48,
                        ),
                        const SizedBox(height: 16),
                        const Text(
                          'QR Code Scanned',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Processing attendance...',
                          style: TextStyle(color: Colors.grey[600]),
                        ),
                      ],
                    )
                  else
                    Column(
                      children: [
                        Icon(
                          Icons.qr_code_scanner,
                          size: 48,
                          color: Theme.of(context).primaryColor,
                        ),
                        const SizedBox(height: 16),
                        const Text(
                          'Scan QR Code',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Point your camera at the QR code to mark attendance',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: Colors.grey[600]),
                        ),
                      ],
                    ),

                  const SizedBox(height: 24),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      CustomButton(
                        text: 'Cancel',
                        onPressed: () => Routes.goBack(context),
                        backgroundColor: Colors.grey,
                        width: 120,
                      ),
                      if (!_isProcessing && !_hasScanned)
                        CustomButton(
                          text: 'Manual Entry',
                          onPressed: () {
                            // TODO: Implement manual entry
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Manual entry feature coming soon!'),
                              ),
                            );
                          },
                          backgroundColor: Colors.orange,
                          width: 120,
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
