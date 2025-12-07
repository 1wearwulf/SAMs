import { create } from 'zustand';
import { api } from '../services/api';
import * as SecureStore from 'expo-secure-store';
import * as Location from 'expo-location';

interface Course {
  id: string;
  name: string;
  attendance: number;
}

interface AttendanceRecord {
  id: string;
  course: string;
  date: string;
  status: 'Present' | 'Absent' | 'Late';
}

interface AppState {
  user: {
    name: string;
    studentId: string;
    email: string;
  } | null;
  courses: Course[];
  attendanceRecords: AttendanceRecord[];
  isLoading: boolean;
  error: string | null;

  // Actions
  setUser: (user: any) => void;
  loadCourses: () => Promise<void>;
  loadAttendance: () => Promise<void>;
  loadUserProfile: () => Promise<void>;
  markAttendance: (qrData: any) => Promise<{ success: boolean; message: string }>;
  logout: () => Promise<void>;
}

export const useStore = create<AppState>((set, get) => ({
  user: {
    name: 'John Doe',
    studentId: '2023001',
    email: 'john.doe@university.edu',
  },
  courses: [],
  attendanceRecords: [],
  isLoading: false,
  error: null,

  setUser: (user) => set({ user }),

  loadCourses: async () => {
    set({ isLoading: true });
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 800));
      set({
        courses: [
          { id: 'CS101', name: 'Computer Science 101', attendance: 92 },
          { id: 'MATH202', name: 'Mathematics 202', attendance: 85 },
          { id: 'PHY101', name: 'Physics 101', attendance: 78 },
          { id: 'ENG201', name: 'Engineering 201', attendance: 95 },
        ],
        isLoading: false
      });
    } catch (error) {
      set({ error: 'Failed to load courses', isLoading: false });
    }
  },

  loadAttendance: async () => {
    set({ isLoading: true });
    try {
      const response = await api.get('/attendance/');
      set({
        attendanceRecords: response.data.map((record: any) => ({
          id: record.id,
          course: record.course_name || record.course,
          date: record.date,
          status: record.status,
        })),
        isLoading: false
      });
    } catch (error) {
      set({ error: 'Failed to load attendance', isLoading: false });
    }
  },

  loadUserProfile: async () => {
    set({ isLoading: true });
    try {
      const response = await api.get('/auth/profile/');
      set({
        user: {
          name: response.data.name,
          studentId: response.data.student_id,
          email: response.data.email,
        },
        isLoading: false
      });
    } catch (error) {
      set({ error: 'Failed to load user profile', isLoading: false });
    }
  },

  markAttendance: async (qrData) => {
    set({ isLoading: true });
    try {
      // Request location permissions
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Location permission denied');
      }

      // Get current location
      const location = await Location.getCurrentPositionAsync({});

      const attendanceData = {
        course_id: qrData.courseId,
        session_id: qrData.sessionId,
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
        timestamp: new Date().toISOString(),
      };

      const response = await api.post('/attendance/mark/', attendanceData);

      set({ isLoading: false });

      // Reload attendance records
      get().loadAttendance();

      return {
        success: true,
        message: 'Attendance marked for ' + (qrData.courseName || qrData.courseId)
      };
    } catch (error) {
      set({ error: 'Failed to mark attendance', isLoading: false });
      return { success: false, message: (error as Error).message || 'Attendance marking failed' };
    }
  },

  logout: async () => {
    try {
      await SecureStore.deleteItemAsync('accessToken');
      await SecureStore.deleteItemAsync('refreshToken');
    } catch (error) {
      console.error('Error clearing tokens:', error);
    }
    set({
      user: null,
      courses: [],
      attendanceRecords: [],
      error: null,
    });
  },
}));
