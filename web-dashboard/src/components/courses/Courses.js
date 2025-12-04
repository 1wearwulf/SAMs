import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const Courses = () => {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Courses Management
            </Typography>
            <Paper sx={{ p: 2, mt: 2 }}>
                <Typography variant="body1">
                    Courses component is under development.
                </Typography>
            </Paper>
        </Box>
    );
};

export default Courses;
