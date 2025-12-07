import { Box, Typography } from '@mui/material';

const Attendance = () => {
  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Attendance Management
      </Typography>
      <Typography variant="body1">
        Attendance module - Under development
      </Typography>
    </Box>
  );
};

export default Attendance;
=======
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    Box,
    Typography,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Button,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    IconButton,
    Chip,
    InputAdornment,
    Alert,
    Skeleton,
    MenuItem,
    FormControl,
    InputLabel,
    Select,
    Card,
    CardContent,
    Grid,
    Tabs,
    Tab,
    Badge,
    LinearProgress,
} from '@mui/material';
import {
    Search,
    FilterList,
    CheckCircle,
    Cancel,
    Schedule,
    LocationOn,
    QrCode,
    Refresh,
    Event,
    People,
} from '@mui/icons-material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { fetchCourses } from '../../store/slices/coursesSlice';
import { fetchStudents } from '../../store/slices/studentsSlice';

const Attendance = () => {
    const dispatch = useDispatch();
    const { courses, loading: coursesLoading } = useSelector((state) => state.courses);
    const { students, loading: studentsLoading } = useSelector((state) => state.students);

    const [activeTab, setActiveTab] = useState(0);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCourse, setSelectedCourse] = useState('');
    const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
    const [attendanceRecords, setAttendanceRecords] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        dispatch(fetchCourses());
        dispatch(fetchStudents());
        loadAttendanceData();
    }, [dispatch, selectedCourse, selectedDate]);

    const loadAttendanceData = async () => {
        setLoading(true);
        try {
            // Simulate API call - replace with real API call
            setTimeout(() => {
                const mockData = generateMockAttendanceData();
                setAttendanceRecords(mockData);
                setLoading(false);
            }, 1000);
        } catch (error) {
            console.error('Failed to load attendance data:', error);
            setLoading(false);
        }
    };

    const generateMockAttendanceData = () => {
        const filteredStudents = selectedCourse
            ? students.filter(s => s.course === selectedCourse)
            : students;

        return filteredStudents.map(student => ({
            id: student.id,
            student: student,
            status: Math.random() > 0.2 ? 'present' : Math.random() > 0.5 ? 'absent' : 'late',
            timestamp: new Date().toISOString(),
            location: {
                lat: 40.7128 + (Math.random() - 0.5) * 0.01,
                lng: -74.0060 + (Math.random() - 0.5) * 0.01,
            },
            device_info: 'Mobile App',
        }));
    };

    const handleTabChange = (event, newValue) => {
        setActiveTab(newValue);
    };

    const filteredRecords = attendanceRecords.filter(record => {
        const matchesSearch = !searchTerm ||
            record.student.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            record.student.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            record.student.student_id.toLowerCase().includes(searchTerm.toLowerCase());

        return matchesSearch;
    });

    const getStatusColor = (status) => {
        switch (status) {
            case 'present': return 'success';
            case 'absent': return 'error';
            case 'late': return 'warning';
            default: return 'default';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'present': return <CheckCircle />;
            case 'absent': return <Cancel />;
            case 'late': return <Schedule />;
            default: return null;
        }
    };

    // Calculate statistics
    const totalStudents = filteredRecords.length;
    const presentCount = filteredRecords.filter(r => r.status === 'present').length;
    const absentCount = filteredRecords.filter(r => r.status === 'absent').length;
    const lateCount = filteredRecords.filter(r => r.status === 'late').length;
    const attendanceRate = totalStudents > 0 ? Math.round((presentCount / totalStudents) * 100) : 0;

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
                    Attendance Monitoring
                </Typography>
                <Button
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={loadAttendanceData}
                    disabled={loading}
                >
                    Refresh
                </Button>
            </Box>

            {/* Statistics Cards */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Total Students
                            </Typography>
                            <Typography variant="h4">
                                {totalStudents}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Present
                            </Typography>
                            <Typography variant="h4" color="success.main">
                                {presentCount}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Absent
                            </Typography>
                            <Typography variant="h4" color="error.main">
                                {absentCount}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Attendance Rate
                            </Typography>
                            <Typography variant="h4" color="primary.main">
                                {attendanceRate}%
                            </Typography>
                            <LinearProgress
                                variant="determinate"
                                value={attendanceRate}
                                sx={{ mt: 1, height: 6, borderRadius: 3 }}
                            />
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Filters */}
            <Paper sx={{ p: 2, mb: 2 }}>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
                    <TextField
                        label="Search Students"
                        variant="outlined"
                        size="small"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <Search />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ minWidth: 250 }}
                    />
                    <FormControl size="small" sx={{ minWidth: 200 }}>
                        <InputLabel>Filter by Course</InputLabel>
                        <Select
                            value={selectedCourse}
                            label="Filter by Course"
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
                    <TextField
                        label="Date"
                        type="date"
                        size="small"
                        value={selectedDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <Event />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ minWidth: 180 }}
                    />
                </Box>
            </Paper>

            {/* Tabs */}
            <Paper sx={{ mb: 2 }}>
                <Tabs value={activeTab} onChange={handleTabChange} aria-label="attendance tabs">
                    <Tab
                        label={
                            <Badge badgeContent={filteredRecords.length} color="primary">
                                Live Attendance
                            </Badge>
                        }
                    />
                    <Tab label="Session History" />
                    <Tab label="Reports" />
                </Tabs>
            </Paper>

            {/* Tab Content */}
            {activeTab === 0 && (
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Student ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Time</TableCell>
                                <TableCell>Location</TableCell>
                                <TableCell>Device</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {loading ? (
                                Array.from({ length: 5 }).map((_, index) => (
                                    <TableRow key={index}>
                                        <TableCell><Skeleton /></TableCell>
                                        <TableCell><Skeleton /></TableCell>
                                        <TableCell><Skeleton /></TableCell>
                                        <TableCell><Skeleton /></TableCell>
                                        <TableCell><Skeleton /></TableCell>
                                        <TableCell><Skeleton /></TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                filteredRecords.map((record) => (
                                    <TableRow key={record.id} hover>
                                        <TableCell>
                                            <Typography variant="body2" fontWeight="bold">
                                                {record.student.student_id}
                                            </Typography>
                                        </TableCell>
                                        <TableCell>
                                            {`${record.student.first_name} ${record.student.last_name}`}
                                        </TableCell>
                                        <TableCell>
                                            <Chip
                                                icon={getStatusIcon(record.status)}
                                                label={record.status}
                                                color={getStatusColor(record.status)}
                                                size="small"
                                                sx={{ textTransform: 'capitalize' }}
                                            />
                                        </TableCell>
                                        <TableCell>
                                            {new Date(record.timestamp).toLocaleTimeString()}
                                        </TableCell>
                                        <TableCell>
                                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                                <LocationOn sx={{ mr: 0.5, fontSize: 16 }} />
                                                <Typography variant="caption">
                                                    {record.location.lat.toFixed(4)}, {record.location.lng.toFixed(4)}
                                                </Typography>
                                            </Box>
                                        </TableCell>
                                        <TableCell>
                                            <Chip
                                                label={record.device_info}
                                                size="small"
                                                variant="outlined"
                                            />
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                            {!loading && filteredRecords.length === 0 && (
                                <TableRow>
                                    <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                                        <Typography variant="body1" color="textSecondary">
                                            No attendance records found
                                        </Typography>
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}

            {activeTab === 1 && (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="h6" color="textSecondary">
                        Session History - Coming Soon
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                        View historical attendance sessions and detailed reports
                    </Typography>
                </Box>
            )}

            {activeTab === 2 && (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="h6" color="textSecondary">
                        Attendance Reports - Coming Soon
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                        Generate and export detailed attendance reports
                    </Typography>
                </Box>
            )}
        </Box>
    );
};

export default Attendance;
