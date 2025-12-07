import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';

// Async thunks
export const fetchAnalytics = createAsyncThunk(
    'analytics/fetchAnalytics',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/analytics/dashboard/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch analytics');
        }
    }
);

export const fetchAttendanceStats = createAsyncThunk(
    'analytics/fetchAttendanceStats',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/analytics/attendance/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch attendance stats');
        }
    }
);

export const fetchCourseStats = createAsyncThunk(
    'analytics/fetchCourseStats',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/analytics/courses/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch course stats');
        }
    }
);

export const fetchStudentStats = createAsyncThunk(
    'analytics/fetchStudentStats',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/analytics/students/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch student stats');
        }
    }
);

// Slice
const analyticsSlice = createSlice({
    name: 'analytics',
    initialState: {
        overview: null,
        attendanceStats: null,
        courseStats: null,
        studentStats: null,
        loading: false,
        error: null,
        dateRange: {
            start: null,
            end: null,
        },
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setDateRange: (state, action) => {
            state.dateRange = action.payload;
        },
        clearAnalytics: (state) => {
            state.overview = null;
            state.attendanceStats = null;
            state.courseStats = null;
            state.studentStats = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch analytics overview
            .addCase(fetchAnalytics.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAnalytics.fulfilled, (state, action) => {
                state.loading = false;
                state.overview = action.payload;
            })
            .addCase(fetchAnalytics.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Fetch attendance stats
            .addCase(fetchAttendanceStats.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAttendanceStats.fulfilled, (state, action) => {
                state.loading = false;
                state.attendanceStats = action.payload;
            })
            .addCase(fetchAttendanceStats.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Fetch course stats
            .addCase(fetchCourseStats.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCourseStats.fulfilled, (state, action) => {
                state.loading = false;
                state.courseStats = action.payload;
            })
            .addCase(fetchCourseStats.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Fetch student stats
            .addCase(fetchStudentStats.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchStudentStats.fulfilled, (state, action) => {
                state.loading = false;
                state.studentStats = action.payload;
            })
            .addCase(fetchStudentStats.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setDateRange, clearAnalytics } = analyticsSlice.actions;
export default analyticsSlice.reducer;
