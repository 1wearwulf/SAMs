import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  IconButton,
  Chip
} from '@mui/material';
import {
  Settings as SettingsIcon,
  People as PeopleIcon,
  School as SchoolIcon,
  Security as SecurityIcon,
  Analytics as AnalyticsIcon,
  PersonAdd as PersonAddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';

const AdminPanel = () => {
  const [lecturers, setLecturers] = useState([
    { id: 1, name: 'Dr. John Smith', email: 'john.smith@uni.edu', department: 'Computer Science', status: 'active' },
    { id: 2, name: 'Prof. Sarah Johnson', email: 'sarah.j@uni.edu', department: 'Mathematics', status: 'active' },
    { id: 3, name: 'Dr. Michael Chen', email: 'm.chen@uni.edu', department: 'Engineering', status: 'inactive' },
  ]);
  
  const [openDialog, setOpenDialog] = useState(false);
  const [currentLecturer, setCurrentLecturer] = useState(null);

  const adminCards = [
    {
      title: 'User Management',
      description: 'Manage all users, roles, and permissions',
      icon: <PeopleIcon />,
      path: '/students'
    },
    {
      title: 'Lecturer Management',
      description: 'Add, edit, and manage lecturers',
      icon: <PersonAddIcon />,
      action: () => setOpenDialog(true)
    },
    {
      title: 'System Settings',
      description: 'Configure system preferences and settings',
      icon: <SettingsIcon />,
      path: '/settings'
    },
    {
      title: 'Course Management',
      description: 'Create and manage courses and enrollments',
      icon: <SchoolIcon />,
      path: '/courses'
    },
    {
      title: 'Security',
      description: 'Manage security settings and access controls',
      icon: <SecurityIcon />,
      path: '/security'
    },
    {
      title: 'Analytics',
      description: 'View system analytics and reports',
      icon: <AnalyticsIcon />,
      path: '/analytics'
    },
  ];

  const handleAddLecturer = () => {
    setCurrentLecturer(null);
    setOpenDialog(true);
  };

  const handleEditLecturer = (lecturer) => {
    setCurrentLecturer(lecturer);
    setOpenDialog(true);
  };

  const handleDeleteLecturer = (id) => {
    if (window.confirm('Are you sure you want to delete this lecturer?')) {
      setLecturers(lecturers.filter(l => l.id !== id));
    }
  };

  const handleSaveLecturer = (data) => {
    if (currentLecturer) {
      // Update existing
      setLecturers(lecturers.map(l => 
        l.id === currentLecturer.id ? { ...l, ...data } : l
      ));
    } else {
      // Add new
      setLecturers([...lecturers, { id: Date.now(), ...data }]);
    }
    setOpenDialog(false);
  };

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Admin Panel
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Manage all aspects of the SAMS system from this panel.
      </Typography>

      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Test Credentials:</strong> 
        <Box component="span" sx={{ ml: 1 }}>
          Admin: admin@sams.edu / admin123 | 
          Lecturer: lecturer@sams.edu / lecturer123 | 
          Student: student@sams.edu / student123
        </Box>
      </Alert>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {adminCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card className="info-card">
              <CardContent>
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Box sx={{ color: 'primary.main' }}>
                    {card.icon}
                  </Box>
                  <Typography variant="h6" fontWeight="bold">
                    {card.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {card.description}
                </Typography>
              </CardContent>
              <Divider />
              <CardActions>
                <Button 
                  size="small" 
                  color="primary"
                  onClick={card.action || (() => window.location.href = card.path)}
                >
                  Manage
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Lecturer Management Section */}
      <Paper sx={{ p: 3, mt: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5" fontWeight="bold">
            Lecturer Management
          </Typography>
          <Button
            variant="contained"
            startIcon={<PersonAddIcon />}
            onClick={handleAddLecturer}
          >
            Add Lecturer
          </Button>
        </Box>

        <Grid container spacing={2}>
          {lecturers.map((lecturer) => (
            <Grid item xs={12} md={6} lg={4} key={lecturer.id}>
              <Card variant="outlined">
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                    <Box>
                      <Typography variant="h6">{lecturer.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {lecturer.email}
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 1 }}>
                        {lecturer.department}
                      </Typography>
                    </Box>
                    <Chip
                      label={lecturer.status}
                      color={lecturer.status === 'active' ? 'success' : 'error'}
                      size="small"
                    />
                  </Box>
                </CardContent>
                <CardActions>
                  <IconButton
                    size="small"
                    onClick={() => handleEditLecturer(lecturer)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDeleteLecturer(lecturer.id)}
                    color="error"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Add/Edit Lecturer Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {currentLecturer ? 'Edit Lecturer' : 'Add New Lecturer'}
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} pt={2}>
            <TextField
              label="Full Name"
              defaultValue={currentLecturer?.name || ''}
              fullWidth
              onChange={(e) => setCurrentLecturer({...currentLecturer, name: e.target.value})}
            />
            <TextField
              label="Email"
              type="email"
              defaultValue={currentLecturer?.email || ''}
              fullWidth
              onChange={(e) => setCurrentLecturer({...currentLecturer, email: e.target.value})}
            />
            <TextField
              label="Department"
              defaultValue={currentLecturer?.department || ''}
              fullWidth
              onChange={(e) => setCurrentLecturer({...currentLecturer, department: e.target.value})}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => handleSaveLecturer(currentLecturer || {})}>
            {currentLecturer ? 'Update' : 'Add'} Lecturer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AdminPanel;
