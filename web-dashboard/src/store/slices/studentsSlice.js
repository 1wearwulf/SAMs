import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';

// Async thunks
export const fetchStudents = createAsyncThunk(
    'students/fetchStudents',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/students/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch students');
        }
    }
);

export const createStudent = createAsyncThunk(
    'students/createStudent',
    async (studentData, { rejectWithValue }) => {
        try {
            const response = await api.post('/students/', studentData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to create student');
        }
    }
);

export const updateStudent = createAsyncThunk(
    'students/updateStudent',
    async ({ id, studentData }, { rejectWithValue }) => {
        try {
            const response = await api.put(`/students/${id}/`, studentData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to update student');
        }
    }
);

export const deleteStudent = createAsyncThunk(
    'students/deleteStudent',
    async (id, { rejectWithValue }) => {
        try {
            await api.delete(`/students/${id}/`);
            return id;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to delete student');
        }
    }
);

// Slice
const studentsSlice = createSlice({
    name: 'students',
    initialState: {
        students: [],
        loading: false,
        error: null,
        selectedStudent: null,
        totalCount: 0,
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setSelectedStudent: (state, action) => {
            state.selectedStudent = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch students
            .addCase(fetchStudents.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchStudents.fulfilled, (state, action) => {
                state.loading = false;
                state.students = action.payload.results || action.payload;
                state.totalCount = action.payload.count || action.payload.length;
            })
            .addCase(fetchStudents.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Create student
            .addCase(createStudent.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createStudent.fulfilled, (state, action) => {
                state.loading = false;
                state.students.push(action.payload);
                state.totalCount += 1;
            })
            .addCase(createStudent.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Update student
            .addCase(updateStudent.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateStudent.fulfilled, (state, action) => {
                state.loading = false;
                const index = state.students.findIndex(student => student.id === action.payload.id);
                if (index !== -1) {
                    state.students[index] = action.payload;
                }
            })
            .addCase(updateStudent.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Delete student
            .addCase(deleteStudent.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteStudent.fulfilled, (state, action) => {
                state.loading = false;
                state.students = state.students.filter(student => student.id !== action.payload);
                state.totalCount -= 1;
            })
            .addCase(deleteStudent.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setSelectedStudent } = studentsSlice.actions;
export default studentsSlice.reducer;
