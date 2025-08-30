import { NavLink, Link } from 'react-router-dom';
import { useState } from 'react';
import styles from './NavBar.module.css';

export default function NavBar() {
  const [open, setOpen] = useState(false);
  const toggle = () => setOpen((o) => !o);
  const close = () => setOpen(false);

  return (
    <header className={styles.navbar}>
      <a href="#main" className="skip-link">Skip to content</a>
      <Link to="/jobs/discover" className={styles.logoLink} onClick={close}>
        <img
          src="/trainium-logo.svg"
          alt="Trainium Career Navigator logo"
          className={styles.logo}
        />
      </Link>
      <button
        className={styles.menuButton}
        aria-label="Toggle menu"
        aria-controls="primary-navigation"
        aria-expanded={open}
        onClick={toggle}
      >
        ☰
      </button>
      <nav
        id="primary-navigation"
        className={`${styles.nav} ${open ? styles.open : ''}`}
      >
        <ul className={styles.links}>
          <li className={styles.link}>
            <NavLink to="/playbook" onClick={close} className={({isActive}) => isActive ? styles.active : undefined}>Career Playbook</NavLink>
          </li>
          <li className={styles.link}>
            <NavLink to="/jobs" onClick={close} className={({isActive}) => isActive ? styles.active : undefined}>Jobs</NavLink>
          </li>
          <li className={styles.link}>
            <NavLink to="/engagement" onClick={close} className={({isActive}) => isActive ? styles.active : undefined}>Engagement</NavLink>
          </li>
          <li className={styles.link}>
            <NavLink to="/contacts" onClick={close} className={({isActive}) => isActive ? styles.active : undefined}>Contacts</NavLink>
          </li>
          <li className={styles.link}>
            <NavLink to="/progress" onClick={close} className={({isActive}) => isActive ? styles.active : undefined}>Progress</NavLink>
          </li>
        </ul>
      </nav>
    </header>
  );
}
