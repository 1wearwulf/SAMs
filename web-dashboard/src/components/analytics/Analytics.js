import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Skeleton,
  Alert,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  People,
  School,
  Assessment,
  Timeline,
  PieChart as PieChartIcon,
  BarChart as BarChartIcon,
} from '@mui/icons-material';
import { fetchCourses } from '../../store/slices/coursesSlice';
import { fetchStudents } from '../../store/slices/studentsSlice';

const Analytics = () => {
  const dispatch = useDispatch();
  const { courses, loading: coursesLoading } = useSelector((state) => state.courses);
  const { students, loading: studentsLoading } = useSelector((state) => state.students);

  const [activeTab, setActiveTab] = useState(0);
  const [selectedPeriod, setSelectedPeriod] = useState('7d');
  const [selectedCourse, setSelectedCourse] = useState('');

  useEffect(() => {
    dispatch(fetchCourses());
    dispatch(fetchStudents());
  }, [dispatch]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Mock data generators - replace with real API calls
  const generateAttendanceTrendData = () => {
    const days = selectedPeriod === '7d' ? 7 : selectedPeriod === '30d' ? 30 : 90;
    const data = [];
    for (let i = days; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      data.push({
        date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        present: Math.floor(Math.random() * 50) + 70,
        absent: Math.floor(Math.random() * 20) + 5,
        late: Math.floor(Math.random() * 15) + 2,
        total: 100,
      });
    }
    return data;
  };

  const generateCoursePerformanceData = () => {
    return courses.map(course => ({
      name: course.code,
      attendance: Math.floor(Math.random() * 30) + 70,
      assignments: Math.floor(Math.random() * 25) + 75,
      participation: Math.floor(Math.random() * 20) + 80,
      students: course.enrolled_students?.length || Math.floor(Math.random() * 30) + 10,
    }));
  };

  const generateStudentDistributionData = () => {
    const total = students.length;
    const excellent = Math.floor(total * 0.3);
    const good = Math.floor(total * 0.4);
    const average = Math.floor(total * 0.2);
    const poor = total - excellent - good - average;

    return [
      { name: 'Excellent (90-100%)', value: excellent, color: '#4caf50' },
      { name: 'Good (80-89%)', value: good, color: '#2196f3' },
      { name: 'Average (70-79%)', value: average, color: '#ff9800' },
      { name: 'Needs Improvement (<70%)', value: poor, color: '#f44336' },
    ];
  };

  const generateMonthlyTrendsData = () => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months.map(month => ({
      month,
      attendance: Math.floor(Math.random() * 20) + 75,
      enrollment: Math.floor(Math.random() * 50) + 200,
      sessions: Math.floor(Math.random() * 10) + 20,
    }));
  };

  const attendanceTrendData = generateAttendanceTrendData();
  const coursePerformanceData = generateCoursePerformanceData();
  const studentDistributionData = generateStudentDistributionData();
  const monthlyTrendsData = generateMonthlyTrendsData();

  // Calculate summary statistics
  const totalStudents = students.length;
  const totalCourses = courses.length;
  const avgAttendance = attendanceTrendData.reduce((sum, day) => sum + day.present, 0) / attendanceTrendData.length;
  const activeCourses = courses.filter(c => c.status === 'active').length;

  if (coursesLoading || studentsLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <Skeleton variant="text" width={300} height={50} />
        <Skeleton variant="rectangular" height={60} sx={{ mt: 2 }} />
        <Skeleton variant="rectangular" height={400} sx={{ mt: 2 }} />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Analytics Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Period</InputLabel>
            <Select
              value={selectedPeriod}
              label="Period"
              onChange={(e) => setSelectedPeriod(e.target.value)}
            >
              <MenuItem value="7d">Last 7 days</MenuItem>
              <MenuItem value="30d">Last 30 days</MenuItem>
              <MenuItem value="90d">Last 90 days</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Course</InputLabel>
            <Select
              value={selectedCourse}
              label="Course"
              onChange={(e) => setSelectedCourse(e.target.value)}
            >
              <MenuItem value="">All Courses</MenuItem>
              {courses.map((course) => (
                <MenuItem key={course.id} value={course.id}>
                  {course.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Students
                  </Typography>
                  <Typography variant="h4">
                    {totalStudents}
                  </Typography>
                </Box>
                <People sx={{ fontSize: 40, color: 'primary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Active Courses
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {activeCourses}
                  </Typography>
                </Box>
                <School sx={{ fontSize: 40, color: 'success.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Attendance
                  </Typography>
                  <Typography variant="h4" color="primary.main">
                    {Math.round(avgAttendance)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={avgAttendance}
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </Box>
                <Assessment sx={{ fontSize: 40, color: 'primary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Sessions
                  </Typography>
                  <Typography variant="h4">
                    {monthlyTrendsData.reduce((sum, month) => sum + month.sessions, 0)}
                  </Typography>
                </Box>
                <Timeline sx={{ fontSize: 40, color: 'secondary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Paper sx={{ mb: 2 }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="analytics tabs">
          <Tab icon={<TrendingUp />} label="Attendance Trends" />
          <Tab icon={<BarChartIcon />} label="Course Performance" />
          <Tab icon={<PieChartIcon />} label="Student Distribution" />
          <Tab icon={<Timeline />} label="Monthly Overview" />
        </Tabs>
      </Paper>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Daily Attendance Trends
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <AreaChart data={attendanceTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="present"
                      stackId="1"
                      stroke="#4caf50"
                      fill="#4caf50"
                      name="Present"
                    />
                    <Area
                      type="monotone"
                      dataKey="late"
                      stackId="1"
                      stroke="#ff9800"
                      fill="#ff9800"
                      name="Late"
                    />
                    <Area
                      type="monotone"
                      dataKey="absent"
                      stackId="1"
                      stroke="#f44336"
                      fill="#f44336"
                      name="Absent"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Course Performance Metrics
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={coursePerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="attendance" fill="#2196f3" name="Attendance %" />
                    <Bar dataKey="assignments" fill="#4caf50" name="Assignments %" />
                    <Bar dataKey="participation" fill="#ff9800" name="Participation %" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Student Enrollment by Course
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={coursePerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="students" fill="#9c27b0" name="Enrolled Students" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Student Performance Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={studentDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {studentDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Performance Summary
                </Typography>
                <Box sx={{ mt: 2 }}>
                  {studentDistributionData.map((item, index) => (
                    <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Box
                        sx={{
                          width: 16,
                          height: 16,
                          backgroundColor: item.color,
                          borderRadius: 1,
                          mr: 2,
                        }}
                      />
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="body2">{item.name}</Typography>
                        <Typography variant="caption" color="textSecondary">
                          {item.value} students ({((item.value / totalStudents) * 100).toFixed(1)}%)
                        </Typography>
                      </Box>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeTab === 3 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Monthly Trends Overview
                </Typography>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={monthlyTrendsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Line
                      yAxisId="left"
                      type="monotone"
                      dataKey="attendance"
                      stroke="#2196f3"
                      strokeWidth={3}
                      name="Attendance Rate %"
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="enrollment"
                      stroke="#4caf50"
                      strokeWidth={3}
                      name="Total Enrollment"
                    />
                    <Line
                      yAxisId="right"
                      type="monotone"
                      dataKey="sessions"
                      stroke="#ff9800"
                      strokeWidth={3}
                      name="Sessions Conducted"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default Analytics;
