/**
 * SAMS API Configuration
 * Central configuration for Django REST Framework API endpoints
 */

export class ApiConfig {
    // Base configuration
    static readonly BASE_URL = 'http://localhost:8000/api';
    static readonly CONNECT_TIMEOUT = 10000; // 10 seconds
    static readonly RECEIVE_TIMEOUT = 10000; // 10 seconds

    // Authentication endpoints
    static readonly LOGIN_ENDPOINT = '/auth/login/';
    static readonly REFRESH_ENDPOINT = '/auth/refresh/';
    static readonly REGISTER_ENDPOINT = '/auth/register/';

    // User management endpoints
    static readonly USERS_ENDPOINT = '/users/';
    static readonly STUDENTS_ENDPOINT = '/accounts/students/';

    // Course endpoints
    static readonly COURSES_ENDPOINT = '/courses/';

    // Attendance endpoints
    static readonly ATTENDANCE_ENDPOINT = '/attendance/';
    static readonly MARK_ATTENDANCE_ENDPOINT = '/attendance/mark/';
    static readonly VERIFY_QR_ENDPOINT = '/attendance/verify/';

    // Device endpoints
    static readonly DEVICES_ENDPOINT = '/devices/';

    // Analytics endpoints
    static readonly ANALYTICS_ENDPOINT = '/analytics/';
    static readonly DASHBOARD_ENDPOINT = '/analytics/dashboard/';
    static readonly REPORTS_ENDPOINT = '/analytics/reports/';

    // Reports endpoints
    static readonly ATTENDANCE_REPORT_ENDPOINT = '/reports/attendance/';

    /**
     * Get default headers for API requests
     */
    static getHeaders(token?: string | null): Record<string, string> {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    /**
     * Get full URL for endpoint
     */
    static getUrl(endpoint: string): string {
        // Remove leading slash if present
        const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
        return `${this.BASE_URL}/${cleanEndpoint}`;
    }

    /**
     * Validate API configuration
     */
    static validateConfig(): boolean {
        try {
            // Check if base URL is accessible (basic validation)
            const url = new URL(this.BASE_URL);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch {
            return false;
        }
    }

    /**
     * Print configuration for debugging
     */
    static printConfig(): void {
        console.log('🔧 SAMS API Configuration:');
        console.log(`   Base URL: ${this.BASE_URL}`);
        console.log(`   Connect Timeout: ${this.CONNECT_TIMEOUT}ms`);
        console.log(`   Receive Timeout: ${this.RECEIVE_TIMEOUT}ms`);
        console.log(`   Login Endpoint: ${this.getUrl(this.LOGIN_ENDPOINT)}`);
        console.log(`   Users Endpoint: ${this.getUrl(this.USERS_ENDPOINT)}`);
        console.log(`   Courses Endpoint: ${this.getUrl(this.COURSES_ENDPOINT)}`);
        console.log(`   Attendance Endpoint: ${this.getUrl(this.ATTENDANCE_ENDPOINT)}`);
    }
}

// Environment-specific configuration
export const getApiConfig = () => {
    // You can add environment-specific logic here
    // For example, different URLs for development, staging, production
    return ApiConfig;
};
