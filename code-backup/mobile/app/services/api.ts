import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = 'http://192.168.1.100:8000/api'; // Django backend URL - Change to your computer's IP address for mobile testing

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(async (config) => {
  try {
    const token = await SecureStore.getItemAsync('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (error) {
    console.error('Error getting token:', error);
  }
  return config;
});

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try to refresh
      try {
        const refreshToken = await SecureStore.getItemAsync('refreshToken');
        if (refreshToken) {
          const refreshResponse = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });
          const newAccessToken = refreshResponse.data.access;
          await SecureStore.setItemAsync('accessToken', newAccessToken);

          // Retry the original request with new token
          error.config.headers.Authorization = `Bearer ${newAccessToken}`;
          return api.request(error.config);
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
      }
    }
    return Promise.reject(error);
  }
);

// Mock API functions for development
export const mockApi = {
  markAttendance: async (qrData: any) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          message: 'Attendance marked successfully',
          data: {
            ...qrData,
            markedAt: new Date().toISOString(),
            attendanceId: 'att_' + Math.random().toString(36).substr(2, 9),
          },
        });
      }, 1000);
    });
  },

  getStudentCourses: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          courses: [
            { id: 'CS101', name: 'Computer Science 101', attendance: 92 },
            { id: 'MATH202', name: 'Mathematics 202', attendance: 85 },
            { id: 'PHY101', name: 'Physics 101', attendance: 78 },
            { id: 'ENG201', name: 'Engineering 201', attendance: 95 },
          ],
        });
      }, 800);
    });
  },

  getAttendanceRecords: async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          records: [
            { id: '1', course: 'CS101', date: '2024-01-15', status: 'Present' },
            { id: '2', course: 'MATH202', date: '2024-01-15', status: 'Present' },
            { id: '3', course: 'PHY101', date: '2024-01-14', status: 'Absent' },
          ],
        });
      }, 800);
    });
  },
};
