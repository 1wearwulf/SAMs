isValid: boolean;
message: string;
action ?: 'attendance' | 'login' | 'enrollment' | 'invalid';
data ?: any;
}
=======
export interface QRValidationResult {
  isValid: boolean;
  message: string;
  action?: 'attendance' | 'login' | 'enrollment' | 'invalid';
  data?: any;
}

export interface QRResult {
  success: boolean;
  data?: string;
  type?: string;
  error?: string;
  timestamp?: Date;
}

export interface ScanHistoryItem {
  id: string;
  timestamp: Date;
  result: QRResult;
  validation: QRValidationResult;
}
