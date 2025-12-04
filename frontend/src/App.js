import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Box,
  Alert,
  CircularProgress
} from '@mui/material';

// Import components
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ForgotPassword from './components/auth/ForgotPassword';
import Dashboard from './components/dashboard/Dashboard';
import AdminPanel from './components/admin/AdminPanel';
import StudentManagement from './components/admin/StudentManagement';
import Attendance from './components/attendance/Attendance';
import Analytics from './components/analytics/Analytics';
import Layout from './components/layout/Layout';

// Create theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#9c27b0',
      light: '#ba68c8',
      dark: '#7b1fa2',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        },
      },
    },
  },
});

// Mock users for testing
const MOCK_USERS = {
  'admin@sams.edu': {
    id: 1,
    username: 'admin',
    email: 'admin@sams.edu',
    first_name: 'System',
    last_name: 'Administrator',
    role: 'admin',
    password: 'admin123'
  },
  'lecturer@sams.edu': {
    id: 2,
    username: 'lecturer',
    email: 'lecturer@sams.edu',
    first_name: 'Dr. John',
    last_name: 'Smith',
    role: 'lecturer',
    password: 'lecturer123'
  },
  'student@sams.edu': {
    id: 3,
    username: 'student',
    email: 'student@sams.edu',
    first_name: 'Alice',
    last_name: 'Johnson',
    role: 'student',
    password: 'student123'
  }
};

// Main App component
function App() {
  const [backendStatus, setBackendStatus] = useState({
    status: 'connected',
    message: '✅ Using mock authentication for testing'
  });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();

    // Simulate backend check (commented out for now)
    /*
    checkBackendStatus();
    */
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/');
      if (response.ok) {
        setBackendStatus({
          status: 'connected',
          message: '✅ Backend connected successfully'
        });
      } else {
        setBackendStatus({
          status: 'error',
          message: '⚠️ Backend responded with error'
        });
      }
    } catch (error) {
      setBackendStatus({
        status: 'error',
        message: '❌ Cannot connect to backend. Using mock authentication for testing.'
      });
    }
  };

  const checkAuthStatus = () => {
    const token = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (token && storedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  };

  const handleLogin = async (email, password) => {
    try {
      // Mock authentication for testing
      const user = MOCK_USERS[email];

      if (user && user.password === password) {
        // Remove password from user object before storing
        const { password: _, ...userWithoutPassword } = user;

        // Generate mock token
        const mockToken = 'mock_jwt_token_' + Date.now();

        localStorage.setItem('token', mockToken);
        localStorage.setItem('user', JSON.stringify(userWithoutPassword));

        setIsAuthenticated(true);
        setUser(userWithoutPassword);

        return {
          success: true,
          user: userWithoutPassword,
          message: `Welcome ${user.first_name}!`
        };
      } else {
        return {
          success: false,
          error: 'Invalid credentials. Try admin@sams.edu / admin123'
        };
      }

      // Uncomment when backend is ready:
      /*
      const response = await fetch('http://localhost:8000/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.access);
        localStorage.setItem('refreshToken', data.refresh);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        setIsAuthenticated(true);
        setUser(data.user);
        return { success: true, user: data.user };
      } else {
        return { success: false, error: data.detail || 'Invalid credentials' };
      }
      */
    } catch (error) {
      return {
        success: false,
        error: 'Network error. Using mock authentication. Try admin@sams.edu / admin123'
      };
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
          flexDirection="column"
          gap={2}
        >
          <CircularProgress size={60} />
          <Box textAlign="center">
            <h2>SAMS Dashboard</h2>
            <p>Loading your experience...</p>
          </Box>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={
              isAuthenticated ? <Navigate to="/dashboard" /> :
                <Login onLogin={handleLogin} backendStatus={backendStatus} />
            } />
            <Route path="/register" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Register />
            } />
            <Route path="/forgot-password" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <ForgotPassword />
            } />

            {/* Protected routes */}
            <Route path="/" element={
              isAuthenticated ? <Layout user={user} onLogout={handleLogout} /> : <Navigate to="/login" />
            }>
              <Route index element={<Navigate to="/dashboard" />} />
              <Route path="dashboard" element={<Dashboard user={user} />} />

              {/* Admin-only routes */}
              {user?.role === 'admin' && (
                <>
                  <Route path="admin" element={<AdminPanel />} />
                  <Route path="students" element={<StudentManagement />} />
                </>
              )}

              {/* Lecturer routes */}
              {(user?.role === 'lecturer' || user?.role === 'admin') && (
                <>
                  <Route path="attendance" element={<Attendance />} />
                </>
              )}

              {/* Common routes */}
              <Route path="analytics" element={<Analytics />} />
              <Route path="courses" element={<Box p={3}><h2>Courses Management</h2></Box>} />
            </Route>

            {/* Catch all */}
            <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
