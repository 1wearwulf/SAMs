import AsyncStorage from '@react-native-async-storage/async-storage';

// Your Django backend URL - UPDATE THIS IF NEEDED
const API_BASE_URL = 'http://10.42.0.1:8000/api';

// Helper for API requests with auth
const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const token = await AsyncStorage.getItem('userToken');
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error: ${response.status} - ${error}`);
  }

  return response.json();
};

// Helper for login (Django REST Framework typically uses token auth)
const getAuthToken = async (username: string, password: string) => {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  return response.json();
};

export const api = {
  // Authentication - adjust based on your actual auth endpoints
  async login(username: string, password: string) {
    try {
      // Try token auth first (common in DRF)
      const data = await getAuthToken(username, password);
      
      // Store token - adjust based on your response structure
      const token = data.token || data.access_token || data.key;
      await AsyncStorage.setItem('userToken', token);
      await AsyncStorage.setItem('userData', JSON.stringify(data.user || { username }));
      
      return data;
    } catch (error) {
      // Fallback to session auth or demo
      console.log('Token auth failed, trying session/auth endpoint');
      
      // Try standard DRF auth endpoint
      const response = await fetch(`${API_BASE_URL}/auth/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      
      if (response.ok) {
        const data = await response.json();
        await AsyncStorage.setItem('userToken', 'session-auth');
        await AsyncStorage.setItem('userData', JSON.stringify(data));
        return data;
      }
      
      throw error;
    }
  },

  async register(userData: any) {
    return apiRequest('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  async logout() {
    try {
      await apiRequest('/auth/logout/', { method: 'POST' });
    } finally {
      await AsyncStorage.removeItem('userToken');
      await AsyncStorage.removeItem('userData');
    }
  },

  // QR Scanning - based on your attendance endpoints
  async scanQR(qrData: string) {
    return apiRequest('/attendance/validate-qr/', {
      method: 'POST',
      body: JSON.stringify({ qr_data: qrData }),
    });
  },

  async markAttendance(data: any) {
    return apiRequest('/attendance/mark/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async getAttendanceStats() {
    return apiRequest('/attendance/stats/');
  },

  // User management
  async getUserProfile() {
    return apiRequest('/accounts/profile/');
  },

  async updateProfile(profileData: any) {
    return apiRequest('/accounts/profile/', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  },

  // Courses
  async getCourses() {
    return apiRequest('/courses/');
  },

  async getUpcomingSessions() {
    return apiRequest('/courses/upcoming-sessions/');
  },

  // Devices
  async registerDevice(deviceData: any) {
    return apiRequest('/devices/', {
      method: 'POST',
      body: JSON.stringify(deviceData),
    });
  },

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/test/`);
      return response.ok;
    } catch {
      try {
        const response = await fetch(`${API_BASE_URL}/`);
        return response.ok;
      } catch {
        return false;
      }
    }
  },
};
