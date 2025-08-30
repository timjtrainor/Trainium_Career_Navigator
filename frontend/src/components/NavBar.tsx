import { useState } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Link,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

const navItems = [
  { to: '/playbook', label: 'Career Playbook' },
  { to: '/jobs', label: 'Jobs' },
  { to: '/engagement', label: 'Engagement' },
  { to: '/contacts', label: 'Contacts' },
  { to: '/progress', label: 'Progress' },
];

export default function NavBar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);
  const isActive = (path: string) =>
    path === '/jobs'
      ? location.pathname.startsWith('/jobs')
      : location.pathname === path;

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center', width: 250 }}>
      <List>
        {navItems.map((item) => (
          <ListItem key={item.to} disablePadding>
            <ListItemButton
              component={RouterLink}
              to={item.to}
              aria-current={isActive(item.to) ? 'page' : undefined}
            >
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box component="header">
      <Link
        href="#main"
        sx={{
          position: 'absolute',
          left: -10000,
          top: 'auto',
          width: 1,
          height: 1,
          overflow: 'hidden',
          '&:focus': {
            left: 0,
            top: 0,
            width: 'auto',
            height: 'auto',
            background: 'background.paper',
            p: 1,
            zIndex: 1000,
          },
        }}
      >
        Skip to content
      </Link>
      <AppBar position="static" color="default" sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Toolbar>
          <Link
            component={RouterLink}
            to="/jobs/discover"
            sx={{ mr: 2, display: 'flex', alignItems: 'center' }}
          >
            <img src="/trainium-logo.svg" alt="Trainium Career Navigator logo" height={32} />
          </Link>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', sm: 'flex' } }}>
            {navItems.map((item) => (
              <Button
                key={item.to}
                component={RouterLink}
                to={item.to}
                aria-current={isActive(item.to) ? 'page' : undefined}
                color="inherit"
                sx={{ fontWeight: isActive(item.to) ? 600 : undefined }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ display: { sm: 'none' }, ml: 'auto' }}
            aria-label="open navigation"
          >
            <MenuIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Drawer
        anchor="left"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        sx={{ display: { sm: 'none' } }}
      >
        {drawer}
      </Drawer>
    </Box>
  );
}

