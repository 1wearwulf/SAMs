import React, { useState, useEffect } from 'react';
import { 
  Text, 
  View, 
  StyleSheet, 
  TouchableOpacity, 
  Alert,
  ActivityIndicator,
  Modal 
} from 'react-native';
import { CameraView, useCameraPermissions, CameraType } from 'expo-camera';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useStore } from '../store/useStore';

export default function ScanScreen() {
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [scanned, setScanned] = useState(false);
  const [scanning, setScanning] = useState(true);
  const [showSuccess, setShowSuccess] = useState(false);
  const [scanResult, setScanResult] = useState<any>(null);
  const router = useRouter();
  const { markAttendance } = useStore();

  useEffect(() => {
    if (!permission) {
      requestPermission();
    }
  }, [permission]);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Ionicons name="camera-off" size={80} color="#999" />
        <Text style={styles.permissionTitle}>Camera Access Required</Text>
        <Text style={styles.permissionText}>
          This app needs camera access to scan QR codes for attendance.
        </Text>
        <TouchableOpacity style={styles.permissionButton} onPress={requestPermission}>
          <Text style={styles.permissionButtonText}>Grant Camera Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const handleBarCodeScanned = async ({ data }: { data: string }) => {
    if (scanned) return;
    
    setScanned(true);
    setScanning(false);
    
    try {
      // Parse QR data
      const qrData = JSON.parse(data);
      
      // Validate QR data structure
      if (!qrData.courseId || !qrData.sessionId) {
        Alert.alert(
          'Invalid QR Code',
          'This QR code is not valid for attendance marking.',
          [{ text: 'OK', onPress: () => resetScanner() }]
        );
        return;
      }

      // Set scan result for success modal
      setScanResult({
        courseName: qrData.courseName || 'Unknown Course',
        courseCode: qrData.courseId,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        date: new Date().toLocaleDateString(),
      });

      // Show success modal
      setShowSuccess(true);

      // In a real app, you would call your API here
      // await markAttendance(qrData);
      
    } catch (error) {
      Alert.alert(
        'Invalid QR Code',
        'Please scan a valid attendance QR code.',
        [{ text: 'OK', onPress: () => resetScanner() }]
      );
    }
  };

  const resetScanner = () => {
    setScanned(false);
    setScanning(true);
    setShowSuccess(false);
    setScanResult(null);
  };

  const toggleCameraFacing = () => {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  };

  const simulateScan = () => {
    handleBarCodeScanned({
      data: JSON.stringify({
        courseId: 'CS101',
        sessionId: 'session_' + Date.now(),
        courseName: 'Computer Science 101',
        timestamp: new Date().toISOString(),
        location: 'Room CS-201',
        instructor: 'Dr. Smith'
      }),
    });
  };

  return (
    <View style={styles.container}>
      {scanning ? (
        <>
          <CameraView
            style={styles.camera}
            facing={facing}
            barcodeScannerSettings={{
              barcodeTypes: ['qr', 'pdf417'],
            }}
            onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
          >
            <View style={styles.overlay}>
              <View style={styles.unfocusedContainer} />
              <View style={styles.middleRow}>
                <View style={styles.unfocusedContainer} />
                <View style={styles.scanArea}>
                  <View style={styles.cornerTL} />
                  <View style={styles.cornerTR} />
                  <View style={styles.cornerBL} />
                  <View style={styles.cornerBR} />
                </View>
                <View style={styles.unfocusedContainer} />
              </View>
              <View style={styles.unfocusedContainer} />
            </View>
            
            <View style={styles.scanInstructions}>
              <Text style={styles.instructionText}>Align QR code within frame</Text>
              <Text style={styles.instructionSubtext}>Ensure good lighting</Text>
            </View>
          </CameraView>

          <View style={styles.controls}>
            <TouchableOpacity style={styles.flipButton} onPress={toggleCameraFacing}>
              <Ionicons name="camera-reverse" size={28} color="white" />
              <Text style={styles.flipText}>Flip Camera</Text>
            </TouchableOpacity>

            <TouchableOpacity style={styles.simulateButton} onPress={simulateScan}>
              <Ionicons name="phone-portrait" size={24} color="#6200ee" />
              <Text style={styles.simulateText}>Simulate Scan</Text>
            </TouchableOpacity>
          </View>
        </>
      ) : (
        <View style={styles.processingContainer}>
          <ActivityIndicator size="large" color="#6200ee" />
          <Text style={styles.processingText}>Processing QR Code...</Text>
        </View>
      )}

      {/* Success Modal */}
      <Modal
        visible={showSuccess}
        transparent={true}
        animationType="slide"
        onRequestClose={resetScanner}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <View style={styles.successIcon}>
              <Ionicons name="checkmark-circle" size={80} color="#4CAF50" />
            </View>
            
            <Text style={styles.successTitle}>Attendance Marked!</Text>
            
            {scanResult && (
              <View style={styles.successDetails}>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Course:</Text>
                  <Text style={styles.detailValue}>{scanResult.courseName}</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Code:</Text>
                  <Text style={styles.detailValue}>{scanResult.courseCode}</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Time:</Text>
                  <Text style={styles.detailValue}>{scanResult.time}</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Date:</Text>
                  <Text style={styles.detailValue}>{scanResult.date}</Text>
                </View>
              </View>
            )}
            
            <Text style={styles.successMessage}>
              Your attendance has been successfully recorded.
            </Text>
            
            <View style={styles.modalButtons}>
              <TouchableOpacity 
                style={styles.modalButtonSecondary} 
                onPress={() => {
                  setShowSuccess(false);
                  router.push('/(tabs)');
                }}
              >
                <Text style={styles.modalButtonSecondaryText}>Go to Home</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.modalButtonPrimary} 
                onPress={resetScanner}
              >
                <Text style={styles.modalButtonPrimaryText}>Scan Another</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
    backgroundColor: '#f5f5f5',
  },
  permissionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
    color: '#333',
  },
  permissionText: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    marginBottom: 30,
    lineHeight: 22,
  },
  permissionButton: {
    backgroundColor: '#6200ee',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 10,
  },
  permissionButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
  },
  unfocusedContainer: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
  },
  middleRow: {
    flexDirection: 'row',
    flex: 2,
  },
  scanArea: {
    flex: 6,
    position: 'relative',
  },
  cornerTL: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: 40,
    height: 40,
    borderTopWidth: 4,
    borderLeftWidth: 4,
    borderColor: '#6200ee',
  },
  cornerTR: {
    position: 'absolute',
    top: 0,
    right: 0,
    width: 40,
    height: 40,
    borderTopWidth: 4,
    borderRightWidth: 4,
    borderColor: '#6200ee',
  },
  cornerBL: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    width: 40,
    height: 40,
    borderBottomWidth: 4,
    borderLeftWidth: 4,
    borderColor: '#6200ee',
  },
  cornerBR: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 40,
    height: 40,
    borderBottomWidth: 4,
    borderRightWidth: 4,
    borderColor: '#6200ee',
  },
  scanInstructions: {
    position: 'absolute',
    bottom: 40,
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  instructionText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 5,
  },
  instructionSubtext: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: 14,
  },
  controls: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
  },
  flipButton: {
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 15,
    borderRadius: 50,
    width: 100,
  },
  flipText: {
    color: 'white',
    fontSize: 12,
    marginTop: 5,
  },
  simulateButton: {
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 50,
    width: 140,
  },
  simulateText: {
    color: '#6200ee',
    fontSize: 12,
    fontWeight: '600',
    marginTop: 5,
  },
  processingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000',
  },
  processingText: {
    color: 'white',
    fontSize: 18,
    marginTop: 20,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.8)',
    padding: 20,
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 30,
    width: '100%',
    alignItems: 'center',
  },
  successIcon: {
    marginBottom: 20,
  },
  successTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
  },
  successDetails: {
    width: '100%',
    backgroundColor: '#f8f9fa',
    borderRadius: 10,
    padding: 20,
    marginBottom: 20,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  detailLabel: {
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  detailValue: {
    fontSize: 16,
    color: '#333',
    fontWeight: '600',
  },
  successMessage: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
    lineHeight: 22,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
  },
  modalButtonSecondary: {
    flex: 1,
    padding: 15,
    borderRadius: 10,
    backgroundColor: '#f0f0f0',
    marginRight: 10,
    alignItems: 'center',
  },
  modalButtonSecondaryText: {
    color: '#666',
    fontSize: 16,
    fontWeight: '600',
  },
  modalButtonPrimary: {
    flex: 1,
    padding: 15,
    borderRadius: 10,
    backgroundColor: '#6200ee',
    marginLeft: 10,
    alignItems: 'center',
  },
  modalButtonPrimaryText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});
