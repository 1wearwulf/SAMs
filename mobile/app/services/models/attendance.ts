/**
 * Attendance record model
 */
export interface AttendanceRecord {
    id: number;
    student: number; // User ID
    session: number; // CourseSession ID
    course: number; // Course ID
    timestamp: string;
    latitude?: number;
    longitude?: number;
    device_fingerprint?: string;
    qr_code_data?: string;
    status: 'present' | 'late' | 'absent';
    is_verified: boolean;
    marked_by?: number; // User ID who marked the attendance
    notes?: string;
}

/**
 * Attendance summary for a student
 */
export interface AttendanceSummary {
    student_id: number;
    student_name: string;
    course_id: number;
    course_name: string;
    total_sessions: number;
    present_count: number;
    late_count: number;
    absent_count: number;
    attendance_percentage: number;
}

/**
 * Attendance marking request
 */
export interface AttendanceMarkRequest {
    qr_code: string;
    latitude?: number;
    longitude?: number;
    device_fingerprint?: string;
}

/**
 * QR code verification response
 */
export interface QRVerificationResponse {
    valid: boolean;
    session_id?: number;
    course_id?: number;
    instructor_name?: string;
    session_title?: string;
    expires_at?: string;
    error?: string;
}

/**
 * Attendance statistics
 */
export interface AttendanceStats {
    total_students: number;
    present_today: number;
    attendance_rate: number;
    course_id?: number;
    session_id?: number;
}

/**
 * Check if attendance record is present
 */
export function isPresent(record: AttendanceRecord): boolean {
    return record.status === 'present';
}

/**
 * Check if attendance record is late
 */
export function isLate(record: AttendanceRecord): boolean {
    return record.status === 'late';
}

/**
 * Check if attendance record is absent
 */
export function isAbsent(record: AttendanceRecord): boolean {
    return record.status === 'absent';
}

/**
 * Calculate attendance percentage
 */
export function calculateAttendancePercentage(
    present: number,
    late: number,
    total: number
): number {
    if (total === 0) return 0;
    // Late counts as half attendance
    const effectiveAttendance = present + (late * 0.5);
    return Math.round((effectiveAttendance / total) * 100);
}

/**
 * Get attendance status display name
 */
export function getAttendanceStatusDisplay(status: 'present' | 'late' | 'absent'): string {
    switch (status) {
        case 'present':
            return 'Present';
        case 'late':
            return 'Late';
        case 'absent':
            return 'Absent';
        default:
            return 'Unknown';
    }
}

/**
 * Get attendance status color (for UI)
 */
export function getAttendanceStatusColor(status: 'present' | 'late' | 'absent'): string {
    switch (status) {
        case 'present':
            return '#4CAF50'; // Green
        case 'late':
            return '#FF9800'; // Orange
        case 'absent':
            return '#F44336'; // Red
        default:
            return '#9E9E9E'; // Grey
    }
}

/**
 * Check if QR code is expired
 */
export function isQRCodeExpired(expiresAt?: string): boolean {
    if (!expiresAt) return false;
    const expiryDate = new Date(expiresAt);
    const now = new Date();
    return now > expiryDate;
}
