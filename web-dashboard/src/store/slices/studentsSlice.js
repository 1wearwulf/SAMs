import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { studentsAPI } from '../../services/api';

// Async thunks
export const fetchStudents = createAsyncThunk(
    'students/fetchStudents',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await studentsAPI.getStudents(params);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to fetch students');
        }
    }
);

export const fetchStudent = createAsyncThunk(
    'students/fetchStudent',
    async (id, { rejectWithValue }) => {
        try {
            const response = await studentsAPI.getStudent(id);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to fetch student');
        }
    }
);

export const createStudent = createAsyncThunk(
    'students/createStudent',
    async (studentData, { rejectWithValue }) => {
        try {
            const response = await studentsAPI.createStudent(studentData);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to create student');
        }
    }
);

export const updateStudent = createAsyncThunk(
    'students/updateStudent',
    async ({ id, data }, { rejectWithValue }) => {
        try {
            const response = await studentsAPI.updateStudent(id, data);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to update student');
        }
    }
);

export const deleteStudent = createAsyncThunk(
    'students/deleteStudent',
    async (id, { rejectWithValue }) => {
        try {
            await studentsAPI.deleteStudent(id);
            return id;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to delete student');
        }
    }
);

// Slice
const studentsSlice = createSlice({
    name: 'students',
    initialState: {
        students: [],
        currentStudent: null,
        loading: false,
        error: null,
        filters: {
            search: '',
            course: '',
            status: '',
        },
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setFilters: (state, action) => {
            state.filters = { ...state.filters, ...action.payload };
        },
        clearFilters: (state) => {
            state.filters = {
                search: '',
                course: '',
                status: '',
            };
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
                state.students = action.payload;
            })
            .addCase(fetchStudents.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Fetch single student
            .addCase(fetchStudent.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchStudent.fulfilled, (state, action) => {
                state.loading = false;
                state.currentStudent = action.payload;
            })
            .addCase(fetchStudent.rejected, (state, action) => {
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
            })
            .addCase(deleteStudent.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setFilters, clearFilters } = studentsSlice.actions;
export default studentsSlice.reducer;
