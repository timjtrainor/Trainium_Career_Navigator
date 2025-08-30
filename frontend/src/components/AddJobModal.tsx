import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

interface Props {
  onClose: () => void;
}

export default function AddJobModal({ onClose }: Props) {
  return (
    <Dialog open onClose={onClose} aria-labelledby="add-job-title">
      <DialogTitle id="add-job-title">Add Job</DialogTitle>
      <DialogContent>
        <Typography>Modal placeholder</Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} autoFocus>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}

