import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const [testUsers, setTestUsers] = useState([]);

  useEffect(() => {
    // Test backend connection
    fetch('http://localhost:8000/api/')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Backend not responding');
      })
      .then(data => {
        setBackendStatus('✅ Connected to Django API');
      })
      .catch(error => {
        setBackendStatus(`❌ ${error.message}`);
      });

    // Check for test users
    const users = [
      { email: 'admin@example.com', password: 'admin123', role: 'Admin' },
      { email: 'student@test.com', password: 'password123', role: 'Student' },
      { email: 'lecturer@test.com', password: 'password123', role: 'Lecturer' }
    ];
    setTestUsers(users);
  }, []);

  const handleLoginTest = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        alert(`Login successful! Welcome ${data.user?.first_name || email}`);
        // Store token
        localStorage.setItem('token', data.access);
        localStorage.setItem('user', JSON.stringify(data.user));
      } else {
        alert(`Login failed: ${data.detail || 'Invalid credentials'}`);
      }
    } catch (error) {
      alert(`Login error: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 Student Attendance Management System</h1>
        <p>A comprehensive solution for tracking student attendance with QR codes and geolocation</p>
        
        <div style={{ 
          backgroundColor: '#282c34', 
          padding: '20px', 
          borderRadius: '10px',
          margin: '20px 0',
          textAlign: 'left',
          maxWidth: '800px'
        }}>
          <h2>�� Development Status</h2>
          
          <div style={{ margin: '15px 0' }}>
            <h3>Backend (Django)</h3>
            <p>{backendStatus}</p>
            <p>API: <a href="http://localhost:8000/api/" target="_blank" rel="noopener noreferrer" style={{ color: '#61dafb' }}>
              http://localhost:8000/api/
            </a></p>
            <p>Admin: <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer" style={{ color: '#61dafb' }}>
              http://localhost:8000/admin/
            </a></p>
          </div>
          
          <div style={{ margin: '15px 0' }}>
            <h3>Frontend (React)</h3>
            <p>✅ Running at <a href="http://localhost:3000" style={{ color: '#61dafb' }}>http://localhost:3000</a></p>
            <p>⏳ Connecting to backend API...</p>
          </div>
          
          <div style={{ margin: '15px 0' }}>
            <h3>📋 Test Users</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {testUsers.map((user, index) => (
                <div key={index} style={{ 
                  backgroundColor: '#20232a', 
                  padding: '10px', 
                  borderRadius: '5px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <div>
                    <strong>{user.role}</strong>
                    <div>Email: {user.email}</div>
                    <div>Password: {user.password}</div>
                  </div>
                  <button 
                    onClick={() => handleLoginTest(user.email, user.password)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: '#61dafb',
                      color: '#20232a',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      fontWeight: 'bold'
                    }}
                  >
                    Test Login
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div style={{ marginTop: '30px' }}>
          <h3>🔧 Quick Setup Commands</h3>
          <pre style={{ 
            backgroundColor: '#20232a', 
            padding: '15px', 
            borderRadius: '5px',
            textAlign: 'left',
            overflowX: 'auto'
          }}>
            <code>
{`# Start Redis
redis-server --daemonize yes

# Backend (new terminal)
cd backend
source venv/bin/activate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm start`}
            </code>
          </pre>
        </div>
      </header>
    </div>
  );
}

export default App;
