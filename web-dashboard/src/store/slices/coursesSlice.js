import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { coursesAPI } from '../../services/api';

// Async thunks
export const fetchCourses = createAsyncThunk(
    'courses/fetchCourses',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await coursesAPI.getCourses(params);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to fetch courses');
        }
    }
);

export const fetchCourse = createAsyncThunk(
    'courses/fetchCourse',
    async (id, { rejectWithValue }) => {
        try {
            const response = await coursesAPI.getCourse(id);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to fetch course');
        }
    }
);

export const createCourse = createAsyncThunk(
    'courses/createCourse',
    async (courseData, { rejectWithValue }) => {
        try {
            const response = await coursesAPI.createCourse(courseData);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to create course');
        }
    }
);

export const updateCourse = createAsyncThunk(
    'courses/updateCourse',
    async ({ id, data }, { rejectWithValue }) => {
        try {
            const response = await coursesAPI.updateCourse(id, data);
            return response;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to update course');
        }
    }
);

export const deleteCourse = createAsyncThunk(
    'courses/deleteCourse',
    async (id, { rejectWithValue }) => {
        try {
            await coursesAPI.deleteCourse(id);
            return id;
        } catch (error) {
            return rejectWithValue(error.message || 'Failed to delete course');
        }
    }
);

// Slice
const coursesSlice = createSlice({
    name: 'courses',
    initialState: {
        courses: [],
        currentCourse: null,
        loading: false,
        error: null,
        filters: {
            search: '',
            status: '',
            instructor: '',
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
                status: '',
                instructor: '',
            };
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch courses
            .addCase(fetchCourses.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCourses.fulfilled, (state, action) => {
                state.loading = false;
                state.courses = action.payload;
            })
            .addCase(fetchCourses.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Fetch single course
            .addCase(fetchCourse.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchCourse.fulfilled, (state, action) => {
                state.loading = false;
                state.currentCourse = action.payload;
            })
            .addCase(fetchCourse.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Create course
            .addCase(createCourse.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createCourse.fulfilled, (state, action) => {
                state.loading = false;
                state.courses.push(action.payload);
            })
            .addCase(createCourse.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Update course
            .addCase(updateCourse.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateCourse.fulfilled, (state, action) => {
                state.loading = false;
                const index = state.courses.findIndex(course => course.id === action.payload.id);
                if (index !== -1) {
                    state.courses[index] = action.payload;
                }
            })
            .addCase(updateCourse.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Delete course
            .addCase(deleteCourse.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(deleteCourse.fulfilled, (state, action) => {
                state.loading = false;
                state.courses = state.courses.filter(course => course.id !== action.payload);
            })
            .addCase(deleteCourse.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setFilters, clearFilters } = coursesSlice.actions;
export default coursesSlice.reducer;
