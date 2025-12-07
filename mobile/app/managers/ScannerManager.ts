import { QRScannerService, QRScanResult } from '../services/QRScannerService';

export enum QRCodeType {
    ATTENDANCE = 'attendance',
    AUTHENTICATION = 'auth',
    COURSE = 'course',
    UNKNOWN = 'unknown'
}

export interface ProcessedQRData {
    type: QRCodeType;
    data: any;
    timestamp: Date;
    valid: boolean;
}

export class ScannerManager {
    private static instance: ScannerManager;
    private qrService: QRScannerService;

    private constructor() {
        this.qrService = QRScannerService.getInstance();
    }

    static getInstance(): ScannerManager {
        if (!ScannerManager.instance) {
            ScannerManager.instance = new ScannerManager();
        }
        return ScannerManager.instance;
    }

    async initialize(): Promise<boolean> {
        return await this.qrService.requestCameraPermission();
    }

    processQRCode(scanResult: QRScanResult): ProcessedQRData {
        const parsedData = this.qrService.parseQRData(scanResult.data);
        const type = this.determineQRType(parsedData);

        return {
            type,
            data: parsedData,
            timestamp: scanResult.timestamp,
            valid: this.validateQRCode(type, parsedData)
        };
    }

    private determineQRType(data: any): QRCodeType {
        if (typeof data === 'object' && data !== null) {
            if (data.type === 'attendance' || data.studentId || data.courseId) {
                return QRCodeType.ATTENDANCE;
            }
            if (data.type === 'auth' || data.token || data.userId) {
                return QRCodeType.AUTHENTICATION;
            }
            if (data.type === 'course' || data.courseCode || data.instructorId) {
                return QRCodeType.COURSE;
            }
        }
        return QRCodeType.UNKNOWN;
    }

    private validateQRCode(type: QRCodeType, data: any): boolean {
        switch (type) {
            case QRCodeType.ATTENDANCE:
                return !!(data.studentId && data.courseId);
            case QRCodeType.AUTHENTICATION:
                return !!(data.token && data.userId);
            case QRCodeType.COURSE:
                return !!(data.courseCode && data.instructorId);
            default:
                return false;
        }
    }

    async handleScanResult(scanResult: QRScanResult): Promise<ProcessedQRData> {
        const processedData = this.processQRCode(scanResult);

        // Log the scan for analytics
        console.log('QR Code scanned:', {
            type: processedData.type,
            valid: processedData.valid,
            timestamp: processedData.timestamp
        });

        // Here you would typically send the data to your backend
        // await this.sendToBackend(processedData);

        return processedData;
    }
}
