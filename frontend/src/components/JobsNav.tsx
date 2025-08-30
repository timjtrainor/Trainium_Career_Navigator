import { NavLink } from 'react-router-dom';
import styles from './JobsNav.module.css';

export default function JobsNav() {
  return (
    <nav className={styles.jobsNav} aria-label="Jobs">
      <ul className={styles.links}>
        <li className={styles.link}>
          <NavLink to="discover" end className={({isActive}) => isActive ? styles.active : undefined}>Discover</NavLink>
        </li>
        <li className={styles.link}>
          <NavLink to="evaluate" className={({isActive}) => isActive ? styles.active : undefined}>Evaluate</NavLink>
        </li>
        <li className={styles.link}>
          <NavLink to="shortlist" className={({isActive}) => isActive ? styles.active : undefined}>Shortlist</NavLink>
        </li>
        <li className={styles.link}>
          <NavLink to="applications" className={({isActive}) => isActive ? styles.active : undefined}>Applications</NavLink>
        </li>
        <li className={styles.link}>
          <NavLink to="interviews" className={({isActive}) => isActive ? styles.active : undefined}>Interviews</NavLink>
        </li>
        <li className={styles.link}>
          <NavLink to="companies" className={({isActive}) => isActive ? styles.active : undefined}>Companies</NavLink>
        </li>
      </ul>
    </nav>
  );
}
