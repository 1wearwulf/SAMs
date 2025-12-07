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
} from '@mui/material';
import {
    Add,
    Edit,
    Delete,
    Search,
    PersonAdd,
    Email,
    School,
} from '@mui/icons-material';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { fetchStudents, createStudent, updateStudent, deleteStudent } from '../../store/slices/studentsSlice';
import { fetchCourses } from '../../store/slices/coursesSlice';

const Students = () => {
    const dispatch = useDispatch();
    const { students, loading, error } = useSelector((state) => state.students);
    const { courses } = useSelector((state) => state.courses);

    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCourse, setSelectedCourse] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [editingStudent, setEditingStudent] = useState(null);
    const [deleteConfirm, setDeleteConfirm] = useState(null);

    useEffect(() => {
        dispatch(fetchStudents());
        dispatch(fetchCourses());
    }, [dispatch]);

    const validationSchema = Yup.object({
        email: Yup.string().email('Invalid email').required('Email is required'),
        first_name: Yup.string().required('First name is required'),
        last_name: Yup.string().required('Last name is required'),
        student_id: Yup.string().required('Student ID is required'),
        course: Yup.string().required('Course is required'),
    });

    const formik = useFormik({
        initialValues: {
            email: '',
            first_name: '',
            last_name: '',
            student_id: '',
            course: '',
        },
        validationSchema,
        onSubmit: async (values) => {
            try {
                if (editingStudent) {
                    await dispatch(updateStudent({ id: editingStudent.id, data: values })).unwrap();
                } else {
                    await dispatch(createStudent(values)).unwrap();
                }
                handleCloseDialog();
                dispatch(fetchStudents());
            } catch (error) {
                console.error('Failed to save student:', error);
            }
        },
    });

    const handleOpenDialog = (student = null) => {
        setEditingStudent(student);
        if (student) {
            formik.setValues({
                email: student.email || '',
                first_name: student.first_name || '',
                last_name: student.last_name || '',
                student_id: student.student_id || '',
                course: student.course || '',
            });
        } else {
            formik.resetForm();
        }
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setEditingStudent(null);
        formik.resetForm();
    };

    const handleDeleteStudent = async (studentId) => {
        try {
            await dispatch(deleteStudent(studentId)).unwrap();
            dispatch(fetchStudents());
            setDeleteConfirm(null);
        } catch (error) {
            console.error('Failed to delete student:', error);
        }
    };

    const filteredStudents = students.filter(student => {
        const matchesSearch = !searchTerm ||
            student.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.student_id.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesCourse = !selectedCourse || student.course === selectedCourse;

        return matchesSearch && matchesCourse;
    });

    if (loading && students.length === 0) {
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
                    Students Management
                </Typography>
                <Button
                    variant="contained"
                    startIcon={<PersonAdd />}
                    onClick={() => handleOpenDialog()}
                >
                    Add Student
                </Button>
            </Box>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {/* Filters */}
            <Paper sx={{ p: 2, mb: 2 }}>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
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
                </Box>
            </Paper>

            {/* Students Table */}
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Student ID</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>Course</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredStudents.map((student) => (
                            <TableRow key={student.id} hover>
                                <TableCell>{student.student_id}</TableCell>
                                <TableCell>{`${student.first_name} ${student.last_name}`}</TableCell>
                                <TableCell>{student.email}</TableCell>
                                <TableCell>
                                    {courses.find(c => c.id === student.course)?.name || 'N/A'}
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={student.is_active ? 'Active' : 'Inactive'}
                                        color={student.is_active ? 'success' : 'default'}
                                        size="small"
                                    />
                                </TableCell>
                                <TableCell align="right">
                                    <IconButton
                                        color="primary"
                                        onClick={() => handleOpenDialog(student)}
                                    >
                                        <Edit />
                                    </IconButton>
                                    <IconButton
                                        color="error"
                                        onClick={() => setDeleteConfirm(student)}
                                    >
                                        <Delete />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                        {filteredStudents.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                                    <Typography variant="body1" color="textSecondary">
                                        No students found
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Add/Edit Student Dialog */}
            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
                <form onSubmit={formik.handleSubmit}>
                    <DialogTitle>
                        {editingStudent ? 'Edit Student' : 'Add New Student'}
                    </DialogTitle>
                    <DialogContent>
                        <Box sx={{ pt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <TextField
                                fullWidth
                                label="Student ID"
                                name="student_id"
                                value={formik.values.student_id}
                                onChange={formik.handleChange}
                                error={formik.touched.student_id && Boolean(formik.errors.student_id)}
                                helperText={formik.touched.student_id && formik.errors.student_id}
                            />
                            <TextField
                                fullWidth
                                label="First Name"
                                name="first_name"
                                value={formik.values.first_name}
                                onChange={formik.handleChange}
                                error={formik.touched.first_name && Boolean(formik.errors.first_name)}
                                helperText={formik.touched.first_name && formik.errors.first_name}
                            />
                            <TextField
                                fullWidth
                                label="Last Name"
                                name="last_name"
                                value={formik.values.last_name}
                                onChange={formik.handleChange}
                                error={formik.touched.last_name && Boolean(formik.errors.last_name)}
                                helperText={formik.touched.last_name && formik.errors.last_name}
                            />
                            <TextField
                                fullWidth
                                label="Email"
                                name="email"
                                type="email"
                                value={formik.values.email}
                                onChange={formik.handleChange}
                                error={formik.touched.email && Boolean(formik.errors.email)}
                                helperText={formik.touched.email && formik.errors.email}
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <Email />
                                        </InputAdornment>
                                    ),
                                }}
                            />
                            <FormControl fullWidth error={formik.touched.course && Boolean(formik.errors.course)}>
                                <InputLabel>Course</InputLabel>
                                <Select
                                    name="course"
                                    value={formik.values.course}
                                    label="Course"
                                    onChange={formik.handleChange}
                                    startAdornment={
                                        <InputAdornment position="start">
                                            <School />
                                        </InputAdornment>
                                    }
                                >
                                    {courses.map((course) => (
                                        <MenuItem key={course.id} value={course.id}>
                                            {course.name}
                                        </MenuItem>
                                    ))}
                                </Select>
                                {formik.touched.course && formik.errors.course && (
                                    <Typography variant="caption" color="error" sx={{ mt: 0.5, ml: 2 }}>
                                        {formik.errors.course}
                                    </Typography>
                                )}
                            </FormControl>
                        </Box>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseDialog}>Cancel</Button>
                        <Button type="submit" variant="contained" disabled={formik.isSubmitting}>
                            {editingStudent ? 'Update' : 'Add'} Student
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>

            {/* Delete Confirmation Dialog */}
            <Dialog open={Boolean(deleteConfirm)} onClose={() => setDeleteConfirm(null)}>
                <DialogTitle>Confirm Delete</DialogTitle>
                <DialogContent>
                    <Typography>
                        Are you sure you want to delete student "{deleteConfirm?.first_name} {deleteConfirm?.last_name}"?
                        This action cannot be undone.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDeleteConfirm(null)}>Cancel</Button>
                    <Button
                        onClick={() => handleDeleteStudent(deleteConfirm.id)}
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

export default Students;
