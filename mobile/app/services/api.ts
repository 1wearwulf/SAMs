import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000/api'; // Change to your backend URL

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
