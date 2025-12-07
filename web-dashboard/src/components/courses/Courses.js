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
} from '@mui/material';
import {
    Add,
    Edit,
    Delete,
    Search,
    School,
    Person,
    Class,
    Schedule,
} from '@mui/icons-material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { fetchCourses, createCourse, updateCourse, deleteCourse } from '../../store/slices/coursesSlice';
import { fetchStudents } from '../../store/slices/studentsSlice';

const Courses = () => {
    const dispatch = useDispatch();
    const { courses, loading, error } = useSelector((state) => state.courses);
    const { students } = useSelector((state) => state.students);

    const [searchTerm, setSearchTerm] = useState('');
    const [selectedStatus, setSelectedStatus] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [editingCourse, setEditingCourse] = useState(null);
    const [deleteConfirm, setDeleteConfirm] = useState(null);

    useEffect(() => {
        dispatch(fetchCourses());
        dispatch(fetchStudents());
    }, [dispatch]);

    const validationSchema = Yup.object({
        code: Yup.string().required('Course code is required'),
        name: Yup.string().required('Course name is required'),
        description: Yup.string().required('Description is required'),
        instructor: Yup.string().required('Instructor is required'),
        max_students: Yup.number().min(1, 'Must have at least 1 student').required('Max students is required'),
        credits: Yup.number().min(1, 'Must have at least 1 credit').max(6, 'Cannot exceed 6 credits').required('Credits is required'),
        status: Yup.string().required('Status is required'),
    });

    const formik = useFormik({
        initialValues: {
            code: '',
            name: '',
            description: '',
            instructor: '',
            max_students: 30,
            credits: 3,
            status: 'active',
        },
        validationSchema,
        onSubmit: async (values) => {
            try {
                if (editingCourse) {
                    await dispatch(updateCourse({ id: editingCourse.id, data: values })).unwrap();
                } else {
                    await dispatch(createCourse(values)).unwrap();
                }
                handleCloseDialog();
                dispatch(fetchCourses());
            } catch (error) {
                console.error('Failed to save course:', error);
            }
        },
    });

    const handleOpenDialog = (course = null) => {
        setEditingCourse(course);
        if (course) {
            formik.setValues({
                code: course.code || '',
                name: course.name || '',
                description: course.description || '',
                instructor: course.instructor || '',
                max_students: course.max_students || 30,
                credits: course.credits || 3,
                status: course.status || 'active',
            });
        } else {
            formik.resetForm();
        }
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setEditingCourse(null);
        formik.resetForm();
    };

    const handleDeleteCourse = async (courseId) => {
        try {
            await dispatch(deleteCourse(courseId)).unwrap();
            dispatch(fetchCourses());
            setDeleteConfirm(null);
        } catch (error) {
            console.error('Failed to delete course:', error);
        }
    };

    const filteredCourses = courses.filter(course => {
        const matchesSearch = !searchTerm ||
            course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
            course.instructor.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesStatus = !selectedStatus || course.status === selectedStatus;

        return matchesSearch && matchesStatus;
    });

    const getStatusColor = (status) => {
        switch (status) {
            case 'active': return 'success';
            case 'inactive': return 'default';
            case 'completed': return 'info';
            case 'cancelled': return 'error';
            default: return 'default';
        }
    };

    // Calculate summary stats
    const totalCourses = courses.length;
    const activeCourses = courses.filter(c => c.status === 'active').length;
    const totalStudents = students.length;

    if (loading && courses.length === 0) {
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
                    Courses Management
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<School />}
                    onClick={() => handleOpenDialog()}
                >
                    Add Course
                </Button>
            </Box>

            {/* Summary Cards */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Total Courses
                            </Typography>
                            <Typography variant="h4">
                                {totalCourses}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={4}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Active Courses
                            </Typography>
                            <Typography variant="h4" color="success.main">
                                {activeCourses}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={4}>
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
            </Grid>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {/* Filters */}
            <Paper sx={{ p: 2, mb: 2 }}>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <TextField
                        label="Search Courses"
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
                        <InputLabel>Filter by Status</InputLabel>
                        <Select
                            value={selectedStatus}
                            label="Filter by Status"
                            onChange={(e) => setSelectedStatus(e.target.value)}
                        >
                            <MenuItem value="">All Status</MenuItem>
                            <MenuItem value="active">Active</MenuItem>
                            <MenuItem value="inactive">Inactive</MenuItem>
                            <MenuItem value="completed">Completed</MenuItem>
                            <MenuItem value="cancelled">Cancelled</MenuItem>
                        </Select>
                    </FormControl>
                </Box>
            </Paper>

            {/* Courses Table */}
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell><strong>Course Code</strong></TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Instructor</TableCell>
                            <TableCell>Students</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Credits</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredCourses.map((course) => (
                            <TableRow key={course.id} hover>
                                <TableCell>
                                    <Typography variant="body2" fontWeight="bold">
                                        {course.code}
                                    </Typography>
                                </TableCell>
                                <TableCell>
                                    <Typography variant="body2" sx={{ maxWidth: 200 }}>
                                        {course.name}
                                    </Typography>
                                    <Typography variant="caption" color="textSecondary" sx={{ display: 'block' }}>
                                        {course.description?.substring(0, 50)}...
                                    </Typography>
                                </TableCell>
                                <TableCell>{course.instructor}</TableCell>
                                <TableCell>
                                    {course.enrolled_students?.length || 0}/{course.max_students}
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={course.status}
                                        color={getStatusColor(course.status)}
                                        size="small"
                                        sx={{ textTransform: 'capitalize' }}
                                    />
                                </TableCell>
                                <TableCell>{course.credits}</TableCell>
                                <TableCell align="right">
                                    <IconButton
                                        color="primary"
                                        onClick={() => handleOpenDialog(course)}
                                    >
                                        <Edit />
                                    </IconButton>
                                    <IconButton
                                        color="error"
                                        onClick={() => setDeleteConfirm(course)}
                                    >
                                        <Delete />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                        {filteredCourses.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                                    <Typography variant="body1" color="textSecondary">
                                        No courses found
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Add/Edit Course Dialog */}
            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
                <form onSubmit={formik.handleSubmit}>
                    <DialogTitle>
                        {editingCourse ? 'Edit Course' : 'Add New Course'}
                    </DialogTitle>
                    <DialogContent>
                        <Box sx={{ pt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Course Code"
                                        name="code"
                                        value={formik.values.code}
                                        onChange={formik.handleChange}
                                        error={formik.touched.code && Boolean(formik.errors.code)}
                                        helperText={formik.touched.code && formik.errors.code}
                                        InputProps={{
                                            startAdornment: (
                                                <InputAdornment position="start">
                                                    <School />
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Credits"
                                        name="credits"
                                        type="number"
                                        value={formik.values.credits}
                                        onChange={formik.handleChange}
                                        error={formik.touched.credits && Boolean(formik.errors.credits)}
                                        helperText={formik.touched.credits && formik.errors.credits}
                                        InputProps={{
                                            startAdornment: (
                                                <InputAdornment position="start">
                                                    <Schedule />
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                            </Grid>

                            <TextField
                                fullWidth
                                label="Course Name"
                                name="name"
                                value={formik.values.name}
                                onChange={formik.handleChange}
                                error={formik.touched.name && Boolean(formik.errors.name)}
                                helperText={formik.touched.name && formik.errors.name}
                            />

                            <TextField
                                fullWidth
                                label="Description"
                                name="description"
                                multiline
                                rows={3}
                                value={formik.values.description}
                                onChange={formik.handleChange}
                                error={formik.touched.description && Boolean(formik.errors.description)}
                                helperText={formik.touched.description && formik.errors.description}
                            />

                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Instructor"
                                        name="instructor"
                                        value={formik.values.instructor}
                                        onChange={formik.handleChange}
                                        error={formik.touched.instructor && Boolean(formik.errors.instructor)}
                                        helperText={formik.touched.instructor && formik.errors.instructor}
                                        InputProps={{
                                            startAdornment: (
                                                <InputAdornment position="start">
                                                    <Person />
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Max Students"
                                        name="max_students"
                                        type="number"
                                        value={formik.values.max_students}
                                        onChange={formik.handleChange}
                                        error={formik.touched.max_students && Boolean(formik.errors.max_students)}
                                        helperText={formik.touched.max_students && formik.errors.max_students}
                                        InputProps={{
                                            startAdornment: (
                                                <InputAdornment position="start">
                                                    <Class />
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                            </Grid>

                            <FormControl fullWidth error={formik.touched.status && Boolean(formik.errors.status)}>
                                <InputLabel>Status</InputLabel>
                                <Select
                                    name="status"
                                    value={formik.values.status}
                                    label="Status"
                                    onChange={formik.handleChange}
                                >
                                    <MenuItem value="active">Active</MenuItem>
                                    <MenuItem value="inactive">Inactive</MenuItem>
                                    <MenuItem value="completed">Completed</MenuItem>
                                    <MenuItem value="cancelled">Cancelled</MenuItem>
                                </Select>
                                {formik.touched.status && formik.errors.status && (
                                    <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                                        {formik.errors.status}
                                    </Typography>
                                )}
                            </FormControl>
                        </Box>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseDialog}>Cancel</Button>
                        <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
                            {editingCourse ? 'Update' : 'Add'} Course
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>

            {/* Delete Confirmation Dialog */}
            <Dialog open={Boolean(deleteConfirm)} onClose={() => setDeleteConfirm(null)}>
                <DialogTitle>Confirm Delete</DialogTitle>
                <DialogContent>
                    <Typography>
                        Are you sure you want to delete course "{deleteConfirm?.name}"?
                        This action cannot be undone and will affect all enrolled students.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDeleteConfirm(null)}>Cancel</Button>
                    <Button
                        onClick={() => handleDeleteCourse(deleteConfirm.id)}
                        color="error"
                        variant="contained"
                    >
                        Delete
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default Courses;
