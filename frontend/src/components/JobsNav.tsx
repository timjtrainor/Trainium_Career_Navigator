import { Tabs, Tab, Box } from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';

const items = [
  { to: 'discover', label: 'Discover' },
  { to: 'evaluate', label: 'Evaluate' },
  { to: 'shortlist', label: 'Shortlist' },
  { to: 'applications', label: 'Applications' },
  { to: 'interviews', label: 'Interviews' },
  { to: 'companies', label: 'Companies' },
];

export default function JobsNav() {
  const location = useLocation();
  const current = location.pathname.split('/')[2] || 'discover';
  return (
    <Box component="nav" aria-label="Jobs" sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Tabs
        value={current}
        variant="scrollable"
        scrollButtons="auto"
      >
        {items.map((item) => (
          <Tab
            key={item.to}
            label={item.label}
            value={item.to}
            component={RouterLink}
            to={item.to}
            aria-current={current === item.to ? 'page' : undefined}
            sx={{ textTransform: 'none' }}
          />
        ))}
      </Tabs>
    </Box>
  );
}

