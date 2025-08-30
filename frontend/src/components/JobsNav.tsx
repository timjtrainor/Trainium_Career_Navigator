import { Link, useLocation } from 'react-router-dom';
import styles from './JobsNav.module.css';

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
    <nav className={styles.nav} aria-label="Jobs">
      <ul className={styles.list}>
        {items.map((item) => (
          <li key={item.to}>
            <Link to={item.to} aria-current={current === item.to ? 'page' : undefined}>
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
