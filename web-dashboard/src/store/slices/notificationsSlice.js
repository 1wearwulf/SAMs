import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';

// Async thunks
export const fetchNotifications = createAsyncThunk(
    'notifications/fetchNotifications',
    async (params = {}, { rejectWithValue }) => {
        try {
            const response = await api.get('/notifications/', { params });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to fetch notifications');
        }
    }
);

export const createNotification = createAsyncThunk(
    'notifications/createNotification',
    async (notificationData, { rejectWithValue }) => {
        try {
            const response = await api.post('/notifications/', notificationData);
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to create notification');
        }
    }
);

export const markAsRead = createAsyncThunk(
    'notifications/markAsRead',
    async (id, { rejectWithValue }) => {
        try {
            const response = await api.patch(`/notifications/${id}/`, { is_read: true });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to mark notification as read');
        }
    }
);

export const markAllAsRead = createAsyncThunk(
    'notifications/markAllAsRead',
    async (_, { rejectWithValue }) => {
        try {
            const response = await api.post('/notifications/mark-all-read/');
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response?.data || 'Failed to mark all notifications as read');
        }
    }
);

// Slice
const notificationsSlice = createSlice({
    name: 'notifications',
    initialState: {
        notifications: [],
        unreadCount: 0,
        loading: false,
        error: null,
        selectedNotification: null,
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setSelectedNotification: (state, action) => {
            state.selectedNotification = action.payload;
        },
        addNotification: (state, action) => {
            state.notifications.unshift(action.payload);
            if (!action.payload.is_read) {
                state.unreadCount += 1;
            }
        },
        updateUnreadCount: (state, action) => {
            state.unreadCount = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            // Fetch notifications
            .addCase(fetchNotifications.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchNotifications.fulfilled, (state, action) => {
                state.loading = false;
                state.notifications = action.payload.results || action.payload;
                state.unreadCount = action.payload.filter(n => !n.is_read).length;
            })
            .addCase(fetchNotifications.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Create notification
            .addCase(createNotification.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createNotification.fulfilled, (state, action) => {
                state.loading = false;
                state.notifications.unshift(action.payload);
                if (!action.payload.is_read) {
                    state.unreadCount += 1;
                }
            })
            .addCase(createNotification.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Mark as read
            .addCase(markAsRead.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(markAsRead.fulfilled, (state, action) => {
                state.loading = false;
                const notification = state.notifications.find(n => n.id === action.payload.id);
                if (notification && !notification.is_read) {
                    notification.is_read = true;
                    state.unreadCount = Math.max(0, state.unreadCount - 1);
                }
            })
            .addCase(markAsRead.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            // Mark all as read
            .addCase(markAllAsRead.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(markAllAsRead.fulfilled, (state, action) => {
                state.loading = false;
                state.notifications.forEach(notification => {
                    notification.is_read = true;
                });
                state.unreadCount = 0;
            })
            .addCase(markAllAsRead.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { clearError, setSelectedNotification, addNotification, updateUnreadCount } = notificationsSlice.actions;
export default notificationsSlice.reducer;
