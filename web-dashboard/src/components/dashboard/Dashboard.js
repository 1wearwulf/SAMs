import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  IconButton,
  Chip,
  Skeleton,
  Alert,
  Button,
} from '@mui/material';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalCourses: 0,
    todayAttendance: 0,
    pendingTasks: 0,
  });

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setStats({
        totalStudents: 125,
        totalCourses: 8,
        todayAttendance: 92,
        pendingTasks: 5,
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <Box p={3}>
        <Skeleton variant="text" width={200} height={50} />
        <Grid container spacing={3} mt={2}>
          {[1, 2, 3, 4].map((item) => (
            <Grid item xs={12} sm={6} md={3} key={item}>
              <Skeleton variant="rectangular" height={120} />
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Students
              </Typography>
              <Typography variant="h4">
                {stats.totalStudents}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Courses
              </Typography>
              <Typography variant="h4">
                {stats.totalCourses}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Today's Attendance
              </Typography>
              <Typography variant="h4">
                {stats.todayAttendance}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Pending Tasks
              </Typography>
              <Typography variant="h4">
                {stats.pendingTasks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box mt={4}>
        <Alert severity="info">
          Welcome to Student Attendance Management System. Dashboard is under development.
        </Alert>
      </Box>
    </Box>
  );
};

export default Dashboard;
