import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  Paper
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  School as SchoolIcon,
  QrCode as QrCodeIcon
} from '@mui/icons-material';

const Dashboard = ({ user }) => {
  const stats = [
    { title: 'Total Courses', value: '12', icon: <SchoolIcon />, color: '#1976d2' },
    { title: 'Students', value: '245', icon: <PeopleIcon />, color: '#4caf50' },
    { title: 'Attendance Today', value: '89%', icon: <QrCodeIcon />, color: '#ff9800' },
    { title: 'Active Sessions', value: '3', icon: <DashboardIcon />, color: '#9c27b0' },
  ];

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Welcome back, {user?.first_name || user?.username}!
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Here's what's happening with your attendance system today.
      </Typography>

      {/* Simple layout without Grid to avoid warnings */}
      <Box sx={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: 3, 
        mt: 2,
        '& > *': {
          flex: '1 1 200px',
          minWidth: '200px'
        }
      }}>
        {stats.map((stat, index) => (
          <Card key={index} className="info-card">
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    {stat.title}
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
                    {stat.value}
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: stat.color }}>
                  {stat.icon}
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>

      <Box sx={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: 3, 
        mt: 3,
        '& > *': {
          flex: '1 1 300px'
        }
      }}>
        <Paper sx={{ p: 3, flexGrow: 2 }}>
          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>
          <Typography color="text.secondary">
            Your dashboard is ready. More features coming soon!
          </Typography>
        </Paper>
        
        <Paper sx={{ p: 3, flexGrow: 1 }}>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Box display="flex" flexDirection="column" gap={2}>
            <Typography color="text.secondary">
              • Create Attendance Session
            </Typography>
            <Typography color="text.secondary">
              • View Reports
            </Typography>
            <Typography color="text.secondary">
              • Manage Courses
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default Dashboard;
