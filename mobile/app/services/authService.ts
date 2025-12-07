import AsyncStorage from '@react-native-async-storage/async-storage';
import { ApiService, ApiResponse } from './apiService';

export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: 'student' | 'lecturer' | 'admin';
    is_active: boolean;
}

export interface AuthTokens {
    access: string;
    refresh: string;
}

export class AuthService {
    private static instance: AuthService;
    private apiService: ApiService;

    // Storage keys
    private readonly TOKEN_KEY = '@auth_token';
    private readonly REFRESH_TOKEN_KEY = '@refresh_token';
    private readonly USER_KEY = '@user_data';

    private constructor() {
        this.apiService = ApiService.getInstance();
    }

    static getInstance(): AuthService {
        if (!AuthService.instance) {
            AuthService.instance = new AuthService();
        }
        return AuthService.instance;
    }

    /**
     * Login user with username and password
     */
    async login(username: string, password: string): Promise<{ success: boolean; error?: string }> {
        try {
            const response: ApiResponse = await this.apiService.login(username, password);

            if (response.success && response.data) {
                const tokens: AuthTokens = {
                    access: response.data.access,
                    refresh: response.data.refresh,
                };

                const user: User = response.data.user;

                await this.saveAuthData(tokens, user);
                return { success: true };
            } else {
                return { success: false, error: response.error || 'Login failed' };
            }
        } catch (error: any) {
            return { success: false, error: error.message || 'Network error' };
        }
    }

    /**
     * Register new user
     */
    async register(userData: {
        username: string;
        email: string;
        password: string;
        first_name: string;
        last_name: string;
        role: 'student' | 'lecturer' | 'admin';
    }): Promise<{ success: boolean; error?: string }> {
        try {
            const response: ApiResponse = await this.apiService.register(userData);

            if (response.success && response.data) {
                const tokens: AuthTokens = {
                    access: response.data.access,
                    refresh: response.data.refresh,
                };

                const user: User = response.data.user;

                await this.saveAuthData(tokens, user);
                return { success: true };
            } else {
                return { success: false, error: response.error || 'Registration failed' };
            }
        } catch (error: any) {
            return { success: false, error: error.message || 'Network error' };
        }
    }

    /**
     * Logout user
     */
    async logout(): Promise<void> {
        try {
            await AsyncStorage.multiRemove([
                this.TOKEN_KEY,
                this.REFRESH_TOKEN_KEY,
                this.USER_KEY,
            ]);
        } catch (error) {
            console.error('Error during logout:', error);
        }
    }

    /**
     * Check if user is logged in
     */
    async isLoggedIn(): Promise<boolean> {
        try {
            const token = await AsyncStorage.getItem(this.TOKEN_KEY);
            return token !== null && token !== '';
        } catch {
            return false;
        }
    }

    /**
     * Get current access token
     */
    async getToken(): Promise<string | null> {
        try {
            return await AsyncStorage.getItem(this.TOKEN_KEY);
        } catch {
            return null;
        }
    }

    /**
     * Get current user data
     */
    async getCurrentUser(): Promise<User | null> {
        try {
            const userJson = await AsyncStorage.getItem(this.USER_KEY);
            if (userJson) {
                return JSON.parse(userJson);
            }
            return null;
        } catch {
            return null;
        }
    }

    /**
     * Refresh access token
     */
    async refreshToken(): Promise<boolean> {
        try {
            const refreshToken = await AsyncStorage.getItem(this.REFRESH_TOKEN_KEY);
            if (!refreshToken) {
                return false;
            }

            const response: ApiResponse = await this.apiService.refreshToken(refreshToken);

            if (response.success && response.data?.access) {
                const currentTokens = await this.getTokens();
                if (currentTokens) {
                    const newTokens: AuthTokens = {
                        ...currentTokens,
                        access: response.data.access,
                    };
                    await this.saveTokens(newTokens);
                    return true;
                }
            }

            return false;
        } catch {
            return false;
        }
    }

    /**
     * Get stored tokens
     */
    private async getTokens(): Promise<AuthTokens | null> {
        try {
            const access = await AsyncStorage.getItem(this.TOKEN_KEY);
            const refresh = await AsyncStorage.getItem(this.REFRESH_TOKEN_KEY);

            if (access && refresh) {
                return { access, refresh };
            }
            return null;
        } catch {
            return null;
        }
    }

    /**
     * Save authentication data
     */
    private async saveAuthData(tokens: AuthTokens, user: User): Promise<void> {
        try {
            await AsyncStorage.setItem(this.TOKEN_KEY, tokens.access);
            await AsyncStorage.setItem(this.REFRESH_TOKEN_KEY, tokens.refresh);
            await AsyncStorage.setItem(this.USER_KEY, JSON.stringify(user));
        } catch (error) {
            console.error('Error saving auth data:', error);
            throw error;
        }
    }

    /**
     * Save tokens only
     */
    private async saveTokens(tokens: AuthTokens): Promise<void> {
        try {
            await AsyncStorage.setItem(this.TOKEN_KEY, tokens.access);
            await AsyncStorage.setItem(this.REFRESH_TOKEN_KEY, tokens.refresh);
        } catch (error) {
            console.error('Error saving tokens:', error);
            throw error;
        }
    }

    /**
     * Make authenticated API call with automatic token refresh
     */
    async authenticatedRequest<T>(
        apiCall: (token: string) => Promise<ApiResponse<T>>
    ): Promise<ApiResponse<T>> {
        let token = await this.getToken();

        if (!token) {
            return { success: false, error: 'No authentication token' };
        }

        let response = await apiCall(token);

        // If token is expired, try to refresh
        if (response.statusCode === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) {
                token = await this.getToken();
                if (token) {
                    response = await apiCall(token);
                }
            }
        }

        return response;
    }
}
