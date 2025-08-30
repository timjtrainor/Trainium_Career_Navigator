import { Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';
import JobsNav from '../components/JobsNav';
import AddJobModal from '../components/AddJobModal';
import styles from './JobsLayout.module.css';

export default function JobsLayout() {
  const location = useLocation();
  const [showModal, setShowModal] = useState(false);
  const isSearchVisible = /\/jobs\/(discover|shortlist)/.test(location.pathname);
  return (
    <div>
      <JobsNav />
      <header className={styles.header}>
        {isSearchVisible && (
          <input
            type="search"
            placeholder="Search jobs"
            aria-label="Search jobs"
            className={styles.search}
          />
        )}
        <button className={styles.addButton} onClick={() => setShowModal(true)}>
          Add Job
        </button>
      </header>
      <main id="main" className={styles.main}>
        <Outlet />
      </main>
      {showModal && <AddJobModal onClose={() => setShowModal(false)} />}
    </div>
  );
}
