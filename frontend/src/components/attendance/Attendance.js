import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip
} from '@mui/material';
import {
  QrCode as QrCodeIcon,
  Schedule as ScheduleIcon,
  LocationOn as LocationIcon,
  Group as GroupIcon
} from '@mui/icons-material';

const Attendance = () => {
  const sessions = [
    {
      id: 1,
      course: 'Mobile App Development',
      code: 'MOB101',
      time: '10:00 AM - 11:30 AM',
      location: 'Lab 301',
      students: 45,
      status: 'active'
    },
    {
      id: 2,
      course: 'Database Systems',
      code: 'DB202',
      time: '2:00 PM - 3:30 PM',
      location: 'Room 205',
      students: 38,
      status: 'upcoming'
    },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" fontWeight="bold">
            Attendance Management
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Create and manage attendance sessions
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<QrCodeIcon />}>
          Create Session
        </Button>
      </Box>

      <Grid container spacing={3}>
        {sessions.map((session) => (
          <Grid item xs={12} md={6} key={session.id}>
            <Card className="info-card">
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {session.course}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {session.code}
                    </Typography>
                  </Box>
                  <Chip
                    label={session.status === 'active' ? 'Active' : 'Upcoming'}
                    color={session.status === 'active' ? 'success' : 'warning'}
                    size="small"
                  />
                </Box>

                <Box display="flex" flexDirection="column" gap={1}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <ScheduleIcon fontSize="small" color="action" />
                    <Typography variant="body2">{session.time}</Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1}>
                    <LocationIcon fontSize="small" color="action" />
                    <Typography variant="body2">{session.location}</Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={1}>
                    <GroupIcon fontSize="small" color="action" />
                    <Typography variant="body2">{session.students} students</Typography>
                  </Box>
                </Box>
              </CardContent>
              <CardActions>
                <Button size="small" color="primary">
                  View QR Code
                </Button>
                <Button size="small">
                  View Attendance
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Attendance;
