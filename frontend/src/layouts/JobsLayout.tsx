import { Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';
import JobsNav from '../components/JobsNav';
import AddJobModal from '../components/AddJobModal';
import { Box, Button, TextField } from '@mui/material';

export default function JobsLayout() {
  const location = useLocation();
  const [showModal, setShowModal] = useState(false);
  const isSearchVisible = /\/jobs\/(discover|shortlist)/.test(location.pathname);
  return (
    <Box>
      <JobsNav />
      <Box
        component="header"
        sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: 2 }}
      >
        {isSearchVisible && (
          <TextField
            type="search"
            placeholder="Search jobs"
            aria-label="Search jobs"
            size="small"
            sx={{ mr: 2 }}
          />
        )}
        <Button variant="contained" onClick={() => setShowModal(true)}>
          Add Job
        </Button>
      </Box>
      <Box component="main" id="main" sx={{ p: 2 }}>
        <Outlet />
      </Box>
      {showModal && <AddJobModal onClose={() => setShowModal(false)} />}
    </Box>
  );
}

