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
        <div>
          {isSearchVisible && (
            <input
              type="search"
              placeholder="Search jobs"
              className={styles.search}
              aria-label="Search jobs"
            />
          )}
        </div>
        <button onClick={() => setShowModal(true)} className={styles.addButton}>Add Job</button>
      </header>
      <main id="main">
        <Outlet />
      </main>
      {showModal && <AddJobModal onClose={() => setShowModal(false)} />}
    </div>
  );
}
