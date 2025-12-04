import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const Students = () => {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Students Management
            </Typography>
            <Paper sx={{ p: 2, mt: 2 }}>
                <Typography variant="body1">
                    Students component is under development.
                </Typography>
            </Paper>
        </Box>
    );
};

export default Students;
