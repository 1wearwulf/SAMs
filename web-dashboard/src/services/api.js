import axios from 'axios';

// Create axios instance
const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => {
        return response.data;
    },
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const response = await axios.post(
                        `${api.defaults.baseURL}/auth/token/refresh/`,
                        { refresh: refreshToken }
                    );

                    const { access } = response.data;
                    localStorage.setItem('access_token', access);

                    // Retry the original request with new token
                    originalRequest.headers.Authorization = `Bearer ${access}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed, logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_data');
                window.location.href = '/login';
            }
        }

        // Create custom error object
        const customError = {
            message: error.response?.data?.detail ||
                error.response?.data?.message ||
                error.response?.data?.error ||
                error.message ||
                'An error occurred',
            status: error.response?.status,
            data: error.response?.data,
        };

        return Promise.reject(customError);
    }
);

// Auth API methods
export const authAPI = {
    login: (email, password) => api.post('/auth/login/', { email, password }),
    logout: () => api.post('/auth/logout/'),
    refreshToken: (refresh) => api.post('/auth/token/refresh/', { refresh }),
    register: (userData) => api.post('/auth/register/', userData),
    updateProfile: (userData) => api.put('/accounts/profile/', userData),
    changePassword: (passwords) => api.post('/accounts/change-password/', passwords),
    validateSession: () => api.get('/auth/validate-session/'),
};

// Courses API methods
export const coursesAPI = {
    getCourses: (params) => api.get('/courses/', { params }),
    getCourse: (id) => api.get(`/courses/${id}/`),
    createCourse: (courseData) => api.post('/courses/', courseData),
    updateCourse: (id, courseData) => api.put(`/courses/${id}/`, courseData),
    deleteCourse: (id) => api.delete(`/courses/${id}/`),
    enrollStudent: (courseId, studentId) => api.post(`/courses/${courseId}/enroll/`, { student_id: studentId }),
    unenrollStudent: (courseId, studentId) => api.post(`/courses/${courseId}/unenroll/`, { student_id: studentId }),
    getEnrolledStudents: (courseId, params) => api.get(`/courses/${courseId}/students/`, { params }),
};

// Attendance API methods
export const attendanceAPI = {
    getSessions: (params) => api.get('/attendance/sessions/', { params }),
    getSession: (id) => api.get(`/attendance/sessions/${id}/`),
    createSession: (sessionData) => api.post('/attendance/sessions/', sessionData),
    updateSession: (id, sessionData) => api.put(`/attendance/sessions/${id}/`, sessionData),
    deleteSession: (id) => api.delete(`/attendance/sessions/${id}/`),
    startSession: (id) => api.post(`/attendance/sessions/${id}/start/`),
    endSession: (id) => api.post(`/attendance/sessions/${id}/end/`),
    generateQR: (id) => api.post(`/attendance/sessions/${id}/generate-qr/`),
    markAttendance: (sessionId, attendanceData) => api.post(`/attendance/sessions/${sessionId}/mark/`, attendanceData),
    bulkMarkAttendance: (sessionId, attendanceList) => api.post(`/attendance/sessions/${sessionId}/bulk-mark/`, { attendance: attendanceList }),
    getSessionAttendance: (sessionId, params) => api.get(`/attendance/sessions/${sessionId}/records/`, { params }),
    getStudentAttendance: (studentId, params) => api.get(`/attendance/students/${studentId}/records/`, { params }),
    getAttendanceSummary: (params) => api.get('/attendance/summary/', { params }),
};

// Students API methods
export const studentsAPI = {
    getStudents: (params) => api.get('/accounts/students/', { params }),
    getStudent: (id) => api.get(`/accounts/students/${id}/`),
    createStudent: (studentData) => api.post('/accounts/students/', studentData),
    updateStudent: (id, studentData) => api.put(`/accounts/students/${id}/`, studentData),
    deleteStudent: (id) => api.delete(`/accounts/students/${id}/`),
    getStudentCourses: (id, params) => api.get(`/accounts/students/${id}/courses/`, { params }),
    getStudentAttendance: (id, params) => api.get(`/accounts/students/${id}/attendance/`, { params }),
    resetPassword: (id) => api.post(`/accounts/students/${id}/reset-password/`),
};

// Analytics API methods
export const analyticsAPI = {
    getDashboardStats: () => api.get('/analytics/dashboard-stats/'),
    getAttendanceTrends: (params) => api.get('/analytics/attendance-trends/', { params }),
    getCourseAnalytics: (courseId, params) => api.get(`/analytics/courses/${courseId}/`, { params }),
    getStudentAnalytics: (studentId, params) => api.get(`/analytics/students/${studentId}/`, { params }),
    getSystemReports: (params) => api.get('/analytics/reports/', { params }),
    exportData: (params) => api.get('/analytics/export/', { params }),
};

// Notifications API methods
export const notificationsAPI = {
    getNotifications: (params) => api.get('/notifications/', { params }),
    markAsRead: (id) => api.post(`/notifications/${id}/mark-read/`),
    markAllAsRead: () => api.post('/notifications/mark-all-read/'),
    deleteNotification: (id) => api.delete(`/notifications/${id}/`),
    getPreferences: () => api.get('/notifications/preferences/'),
    updatePreferences: (preferences) => api.put('/notifications/preferences/', preferences),
    sendNotification: (notificationData) => api.post('/notifications/send/', notificationData),
};

export { api };
