import { Drawer, Box, Button, Typography } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';

export default function JobDrawer() {
  const { id } = useParams();
  const navigate = useNavigate();
  const onClose = () => navigate(-1);

  return (
    <Drawer anchor="right" open onClose={onClose} PaperProps={{ sx: { width: 300 } }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Job Detail {id}
        </Typography>
        <Button onClick={onClose}>Close</Button>
      </Box>
    </Drawer>
  );
}

