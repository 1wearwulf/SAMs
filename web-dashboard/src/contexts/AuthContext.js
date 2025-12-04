import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    // Check authentication status on mount
    useEffect(() => {
        checkAuthStatus();
    }, []);

    const checkAuthStatus = async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                setLoading(false);
                return;
            }

            // Verify token with backend
            const response = await api.get('/auth/validate-session/');
            if (response.valid) {
                const userData = JSON.parse(localStorage.getItem('user_data') || '{}');
                setUser(userData);
                setIsAuthenticated(true);
            } else {
                // Token invalid, clear storage
                logout();
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        try {
            setLoading(true);
            const response = await api.post('/auth/login/', {
                email,
                password,
            });

            const { user: userData, tokens } = response;

            // Store tokens
            localStorage.setItem('access_token', tokens.access);
            localStorage.setItem('refresh_token', tokens.refresh);
            localStorage.setItem('user_data', JSON.stringify(userData));

            // Set state
            setUser(userData);
            setIsAuthenticated(true);

            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Login failed',
            };
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        try {
            // Call logout endpoint
            await api.post('/auth/logout/');
        } catch (error) {
            console.error('Logout API call failed:', error);
        } finally {
            // Clear local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_data');

            // Reset state
            setUser(null);
            setIsAuthenticated(false);
            setLoading(false);
        }
    };

    const refreshToken = async () => {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
                throw new Error('No refresh token available');
            }

            const response = await api.post('/auth/token/refresh/', {
                refresh: refreshToken,
            });

            const { access } = response;
            localStorage.setItem('access_token', access);

            return access;
        } catch (error) {
            console.error('Token refresh failed:', error);
            logout();
            throw error;
        }
    };

    const updateProfile = async (userData) => {
        try {
            setLoading(true);
            const response = await api.put('/accounts/profile/', userData);

            // Update stored user data
            const updatedUser = { ...user, ...response };
            localStorage.setItem('user_data', JSON.stringify(updatedUser));
            setUser(updatedUser);

            return { success: true, user: updatedUser };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Profile update failed',
            };
        } finally {
            setLoading(false);
        }
    };

    const changePassword = async (currentPassword, newPassword) => {
        try {
            setLoading(true);
            await api.post('/accounts/change-password/', {
                current_password: currentPassword,
                new_password: newPassword,
            });

            return { success: true };
        } catch (error) {
            return {
                success: false,
                error: error.message || 'Password change failed',
            };
        } finally {
            setLoading(false);
        }
    };

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        logout,
        refreshToken,
        updateProfile,
        changePassword,
        checkAuthStatus,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
