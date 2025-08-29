import { NavLink, useLocation } from 'react-router-dom';
import { useState } from 'react';
import styles from './Header.module.css';
import AddJobModal from './AddJobModal';

export default function Header() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const showSearch = location.pathname.startsWith('/jobs/discover') || location.pathname.startsWith('/jobs/shortlist');

  return (
    <header className={styles.header}>
      <div className={styles.brand}>Trainium</div>
      <button className={styles.menu} onClick={() => setMenuOpen(o => !o)} aria-label="Menu">☰</button>
      <nav className={`${styles.nav} ${menuOpen ? styles.open : ''}`}>
        <NavLink to="/jobs/discover" className={({isActive}) => isActive ? styles.active : undefined}>Discover</NavLink>
        <NavLink to="/jobs/evaluate" className={({isActive}) => isActive ? styles.active : undefined}>Evaluate</NavLink>
        <NavLink to="/jobs/shortlist" className={({isActive}) => isActive ? styles.active : undefined}>Shortlist</NavLink>
        <NavLink to="/jobs/applications" className={({isActive}) => isActive ? styles.active : undefined}>Applications</NavLink>
        <NavLink to="/jobs/interviews" className={({isActive}) => isActive ? styles.active : undefined}>Interviews</NavLink>
        <NavLink to="/jobs/companies" className={({isActive}) => isActive ? styles.active : undefined}>Companies</NavLink>
        <NavLink to="/progress" className={({isActive}) => isActive ? styles.active : undefined}>Progress</NavLink>
        <NavLink to="/playbook" className={({isActive}) => isActive ? styles.active : undefined}>Playbook</NavLink>
        <NavLink to="/engagement" className={({isActive}) => isActive ? styles.active : undefined}>Engagement</NavLink>
        <NavLink to="/contacts" className={({isActive}) => isActive ? styles.active : undefined}>Contacts</NavLink>
      </nav>
      <div className={styles.spacer} />
      {showSearch && <input className={styles.search} type="search" placeholder="Search jobs" />}
      <a href="#" className={styles.help}>Help</a>
      <button className={styles.cta} onClick={() => setShowModal(true)}>Add Job</button>
      {showModal && <AddJobModal onClose={() => setShowModal(false)} />}
    </header>
  );
}
