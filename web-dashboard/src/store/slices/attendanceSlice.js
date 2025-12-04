import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';

// Async thunks
export const fetchAttendance = createAsyncThunk(
    'attendance/fetchAttendance',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/attendance/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch attendance');
        }
    }
);

export const markAttendance = createAsyncThunk(
    'attendance/markAttendance',
    async (attendanceData, { rejectWithValue }) => {
        try {
            const response = await api.post('/attendance/', attendanceData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to mark attendance');
        }
    }
);

export const updateAttendance = createAsyncThunk(
    'attendance/updateAttendance',
    async ({ id, attendanceData }, { rejectWithValue }) => {
        try {
            const response = await api.put(`/attendance/${id}/`, attendanceData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to update attendance');
        }
    }
);

// Slice
const attendanceSlice = createSlice({
    name: 'attendance',
    initialState: {
        attendance: [],
        loading: false,
        error: null,
        selectedAttendance: null,
        stats: {
            totalSessions: 0,
            totalStudents: 0,
            presentToday: 0,
            absentToday: 0,
        },
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setSelectedAttendance: (state, action) => {
            state.selectedAttendance = action.payload;
        },
        updateStats: (state, action) => {
            state.stats = { ...state.stats, ...action.payload };
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch attendance
            .addCase(fetchAttendance.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAttendance.fulfilled, (state, action) => {
                state.loading = false;
                state.attendance = action.payload;
            })
            .addCase(fetchAttendance.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Mark attendance
            .addCase(markAttendance.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(markAttendance.fulfilled, (state, action) => {
                state.loading = false;
                state.attendance.push(action.payload);
            })
            .addCase(markAttendance.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Update attendance
            .addCase(updateAttendance.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateAttendance.fulfilled, (state, action) => {
                state.loading = false;
                const index = state.attendance.findIndex(att => att.id === action.payload.id);
                if (index !== -1) {
                    state.attendance[index] = action.payload;
                }
            })
            .addCase(updateAttendance.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setSelectedAttendance, updateStats } = attendanceSlice.actions;
export default attendanceSlice.reducer;
