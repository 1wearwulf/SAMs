import { create } from 'zustand';

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
  markAttendance: (qrData: any) => Promise<{ success: boolean; message: string }>;
  logout: () => void;
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
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 800));
      set({ 
        attendanceRecords: [
          { id: '1', course: 'CS101', date: '2024-01-15', status: 'Present' },
          { id: '2', course: 'MATH202', date: '2024-01-15', status: 'Present' },
          { id: '3', course: 'PHY101', date: '2024-01-14', status: 'Absent' },
        ], 
        isLoading: false 
      });
    } catch (error) {
      set({ error: 'Failed to load attendance', isLoading: false });
    }
  },

  markAttendance: async (qrData) => {
    set({ isLoading: true });
    try {
      // Mock API call - in real app, this would be your backend
      await new Promise(resolve => setTimeout(resolve, 1000));
      set({ isLoading: false });
      
      // Add to attendance records
      const newRecord = {
        id: 'att_' + Date.now(),
        course: qrData.courseId,
        date: new Date().toISOString().split('T')[0],
        status: 'Present' as const,
      };
      
      set(state => ({
        attendanceRecords: [newRecord, ...state.attendanceRecords]
      }));
      
      return { 
        success: true, 
        message: 'Attendance marked for ' + (qrData.courseName || qrData.courseId)
      };
    } catch (error) {
      set({ error: 'Failed to mark attendance', isLoading: false });
      return { success: false, message: 'Attendance marking failed' };
    }
  },

  logout: () => {
    set({
      user: null,
      courses: [],
      attendanceRecords: [],
      error: null,
    });
  },
}));
