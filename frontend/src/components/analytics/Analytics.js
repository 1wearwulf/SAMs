import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Equalizer as EqualizerIcon
} from '@mui/icons-material';

const Analytics = () => {
  const attendanceData = [
    { course: 'Mobile App Development', present: 42, total: 45, percentage: 93 },
    { course: 'Database Systems', present: 35, total: 38, percentage: 92 },
    { course: 'Web Development', present: 40, total: 48, percentage: 83 },
    { course: 'Data Structures', present: 38, total: 42, percentage: 90 },
  ];

  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Analytics Dashboard
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        View attendance statistics and trends
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={3}>
          <Card className="info-card">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Overall Attendance
              </Typography>
              <Typography variant="h3" fontWeight="bold" color="primary">
                89.5%
              </Typography>
              <Box display="flex" alignItems="center" mt={1}>
                <TrendingUpIcon color="success" />
                <Typography variant="body2" color="success.main" ml={1}>
                  +2.5% from last week
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={9}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Course-wise Attendance
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Course</TableCell>
                    <TableCell>Present</TableCell>
                    <TableCell>Total</TableCell>
                    <TableCell>Percentage</TableCell>
                    <TableCell>Progress</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {attendanceData.map((row, index) => (
                    <TableRow key={index}>
                      <TableCell>{row.course}</TableCell>
                      <TableCell>{row.present}</TableCell>
                      <TableCell>{row.total}</TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          {row.percentage}%
                          {row.percentage > 85 ? (
                            <TrendingUpIcon color="success" fontSize="small" sx={{ ml: 1 }} />
                          ) : (
                            <TrendingDownIcon color="error" fontSize="small" sx={{ ml: 1 }} />
                          )}
                        </Box>
                      </TableCell>
                      <TableCell>
                        <LinearProgress 
                          variant="determinate" 
                          value={row.percentage} 
                          color={row.percentage > 85 ? "success" : "warning"}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;
