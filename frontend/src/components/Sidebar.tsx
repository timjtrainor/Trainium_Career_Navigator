import { NavLink } from 'react-router-dom';
import styles from './Sidebar.module.css';

export default function Sidebar() {
  return (
    <nav className={styles.sidebar} aria-label="Main">
      <a href="#main" className={styles.skipLink}>
        Skip to content
      </a>
      <NavLink to="/jobs/discover" className={styles.logo}>
        <img
          src="/trainium-logo.svg"
          alt="Trainium Career Navigator logo"
          height={32}
        />
      </NavLink>
      <ul className={styles.navGroup}>
        <li>
          <NavLink to="/playbook" className={({ isActive }) => isActive ? styles.active : undefined}>
            Career Playbook
          </NavLink>
        </li>
      </ul>
      <div className={styles.section}>Jobs Pipeline</div>
      <ul className={styles.navGroup}>
        <li>
          <NavLink to="/jobs/discover" className={({ isActive }) => isActive ? styles.active : undefined} end>
            Discover
          </NavLink>
        </li>
        <li>
          <NavLink to="/jobs/evaluate" className={({ isActive }) => isActive ? styles.active : undefined}>
            Evaluate
          </NavLink>
        </li>
        <li>
          <NavLink to="/jobs/shortlist" className={({ isActive }) => isActive ? styles.active : undefined}>
            Shortlist
          </NavLink>
        </li>
        <li>
          <NavLink to="/jobs/applications" className={({ isActive }) => isActive ? styles.active : undefined}>
            Applications
          </NavLink>
        </li>
        <li>
          <NavLink to="/jobs/interviews" className={({ isActive }) => isActive ? styles.active : undefined}>
            Interviews
          </NavLink>
        </li>
        <li>
          <NavLink to="/jobs/companies" className={({ isActive }) => isActive ? styles.active : undefined}>
            Companies
          </NavLink>
        </li>
      </ul>
      <ul className={styles.navGroup}>
        <li>
          <NavLink to="/engagement" className={({ isActive }) => isActive ? styles.active : undefined}>
            Engagement
          </NavLink>
        </li>
        <li>
          <NavLink to="/contacts" className={({ isActive }) => isActive ? styles.active : undefined}>
            Contacts
          </NavLink>
        </li>
        <li>
          <NavLink to="/progress" className={({ isActive }) => isActive ? styles.active : undefined}>
            Progress
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

