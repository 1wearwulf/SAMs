import { createSlice } from '@reduxjs/toolkit';

const uiSlice = createSlice({
    name: 'ui',
    initialState: {
        sidebarOpen: true,
        theme: 'light',
        loading: false,
        modal: {
            isOpen: false,
            type: null,
            data: null,
        },
        notifications: {
            show: false,
            type: 'info', // 'success', 'error', 'warning', 'info'
            message: '',
        },
        drawer: {
            isOpen: false,
            type: null,
            data: null,
        },
    },
    reducers: {
        toggleSidebar: (state) => {
            state.sidebarOpen = !state.sidebarOpen;
        },
        setSidebarOpen: (state, action) => {
            state.sidebarOpen = action.payload;
        },
        setTheme: (state, action) => {
            state.theme = action.payload;
        },
        setLoading: (state, action) => {
            state.loading = action.payload;
        },
        openModal: (state, action) => {
            state.modal = {
                isOpen: true,
                type: action.payload.type,
                data: action.payload.data || null,
            };
        },
        closeModal: (state) => {
            state.modal = {
                isOpen: false,
                type: null,
                data: null,
            };
        },
        showNotification: (state, action) => {
            state.notifications = {
                show: true,
                type: action.payload.type || 'info',
                message: action.payload.message,
            };
        },
        hideNotification: (state) => {
            state.notifications.show = false;
        },
        openDrawer: (state, action) => {
            state.drawer = {
                isOpen: true,
                type: action.payload.type,
                data: action.payload.data || null,
            };
        },
        closeDrawer: (state) => {
            state.drawer = {
                isOpen: false,
                type: null,
                data: null,
            };
        },
    },
});

export const {
    toggleSidebar,
    setSidebarOpen,
    setTheme,
    setLoading,
    openModal,
    closeModal,
    showNotification,
    hideNotification,
    openDrawer,
    closeDrawer,
} = uiSlice.actions;

export default uiSlice.reducer;
