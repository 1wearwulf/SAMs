import AsyncStorage from '@react-native-async-storage/async-storage';
import { QRScannerService, QRResult } from './QRScannerService';

export type ScanHistoryItem = QRResult & {
    id: string;
    synced: boolean;
    deviceId?: string;
};

export class ScannerManager {
    private static readonly SCAN_HISTORY_KEY = '@sams_scan_history';
    private static readonly MAX_HISTORY = 100;

    static async processScan(
        rawData: string,
        type: string
    ): Promise<{
        success: boolean;
        result?: QRResult;
        error?: string;
        action?: string;
    }> {
        try {
            // Basic validation
            const validation = QRScannerService.validateQRData(rawData);
            if (!validation.isValid) {
                return {
                    success: false,
                    error: validation.message || 'Invalid QR format',
                };
            }

            // Parse QR data
            const result = QRScannerService.parseQRData(rawData);

            // Provide haptic feedback
            QRScannerService.provideFeedback(result.isValid);

            // Save to history
            await this.saveToHistory(result);

            // Determine action
            const action = this.getActionForResult(result);

            return {
                success: true,
                result,
                action,
            };

        } catch (error) {
            console.error('Scan processing error:', error);
            return {
                success: false,
                error: error.message || 'Failed to process QR code',
            };
        }
    }

    private static async saveToHistory(result: QRResult): Promise<void> {
        try {
            const history = await this.getScanHistory();

            const historyItem: ScanHistoryItem = {
                ...result,
                id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
                synced: false,
                deviceId: 'test-device', // In real app, get actual device ID
            };

            // Keep only recent scans
            const updatedHistory = [historyItem, ...history.slice(0, this.MAX_HISTORY - 1)];

            await AsyncStorage.setItem(
                this.SCAN_HISTORY_KEY,
                JSON.stringify(updatedHistory)
            );
        } catch (error) {
            console.error('Failed to save scan history:', error);
        }
    }

    static async getScanHistory(): Promise<ScanHistoryItem[]> {
        try {
            const history = await AsyncStorage.getItem(this.SCAN_HISTORY_KEY);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Failed to get scan history:', error);
            return [];
        }
    }

    static async clearHistory(): Promise<void> {
        try {
            await AsyncStorage.removeItem(this.SCAN_HISTORY_KEY);
        } catch (error) {
            console.error('Failed to clear history:', error);
        }
    }

    private static getActionForResult(result: QRResult): string {
        switch (result.type) {
            case 'attendance':
                return 'MARK_ATTENDANCE';
            case 'authentication':
                return 'AUTHENTICATE_USER';
            case 'course':
                return 'ENROLL_COURSE';
            case 'url':
                return 'OPEN_URL';
            default:
                return 'PROCESS_TEXT';
        }
    }

    static getTestQRCode(type: 'attendance' | 'auth' | 'course'): string {
        return QRScannerService.generateTestQR(type);
    }

    static validateUserRole(
        userRole: 'student' | 'lecturer' | 'admin',
        scanType: string
    ): boolean {
        const permissions = {
            student: ['attendance'],
            lecturer: ['attendance', 'course'],
            admin: ['attendance', 'course', 'authentication'],
        };

        return permissions[userRole]?.includes(scanType) || false;
    }
}
