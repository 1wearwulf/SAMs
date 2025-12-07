* Show permission denied alert
    */
showPermissionDeniedAlert(): void {
    Alert.alert(
        'Camera Permission Required',
        'Camera access is required to scan QR codes. Please enable camera permissions in your device settings.',
        [
            { text: 'Cancel', style: 'cancel' },
            {
                text: 'Settings', onPress: () => {
                    // Note: In a real app, you might want to open device settings here
                    console.log('Open device settings');
                }
            }
        ]
    );
}
=======
  /**
   * Show permission denied alert
   */
  showPermissionDeniedAlert(): void {
    Alert.alert(
      'Camera Permission Required',
      'Camera access is required to scan QR codes. Please enable camera permissions in your device settings.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Settings', onPress: () => {
          // Note: In a real app, you might want to open device settings here
          console.log('Open device settings');
        }}
      ]
    );
  }

  /**
   * Handle scan result (legacy method for compatibility)
   */
  async handleScan(result: any): Promise<void> {
    try {
      const validation = await this.processScan(result);
      // Add to scan history
      const qrResult: QRResult = {
        success: result.success || false,
        data: result.data,
        type: result.type,
        timestamp: new Date()
      };
      this.scannerService.addToScanHistory(qrResult, validation);
    } catch (error) {
      console.error('Error handling scan:', error);
    }
  }

  /**
   * Handle attendance scan specifically
   */
  async handleAttendanceScan(result: any): Promise<void> {
    const validation = await this.processScan(result);
    if (validation.action === 'attendance' && validation.isValid) {
      // Handle attendance logic here
      console.log('Attendance recorded:', validation.data);
    }
  }

  /**
   * Show error alert
   */
  showErrorAlert(message: string): void {
    this.scannerService.showScanError(message);
  }

  /**
   * Show success alert
   */
  showSuccessAlert(message: string): void {
    this.scannerService.showScanSuccess(message);
  }
