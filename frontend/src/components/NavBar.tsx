import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './NavBar.module.css';

const navItems = [
  { to: '/playbook', label: 'Career Playbook' },
  { to: '/jobs', label: 'Jobs' },
  { to: '/engagement', label: 'Engagement' },
  { to: '/contacts', label: 'Contacts' },
  { to: '/progress', label: 'Progress' },
];

export default function NavBar() {
  const [open, setOpen] = useState(false);
  const location = useLocation();
  const isActive = (path: string) =>
    path === '/jobs'
      ? location.pathname.startsWith('/jobs')
      : location.pathname === path;

  return (
    <header className={styles.header}>
      <a href="#main" className={styles.skipLink}>
        Skip to content
      </a>
      <div className={styles.bar}>
        <Link to="/jobs/discover" className={styles.logo}>
          <img src="/trainium-logo.svg" alt="Trainium Career Navigator logo" height={32} />
        </Link>
        <nav className={`${styles.navLinks} ${open ? styles.open : ''}`} aria-label="Primary">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              aria-current={isActive(item.to) ? 'page' : undefined}
              onClick={() => setOpen(false)}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <button
          className={styles.navButton}
          aria-label="Toggle navigation"
          onClick={() => setOpen(!open)}
        >
          ☰
        </button>
      </div>
    </header>
  );
}
