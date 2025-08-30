import { Outlet, useLocation, useSearchParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import JobsNav from '../components/JobsNav';
import AddJobModal from '../components/AddJobModal';
import styles from './JobsLayout.module.css';

export default function JobsLayout() {
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState(searchParams.get('query') || '');
  const [showModal, setShowModal] = useState(false);
  const isSearchVisible = /\/jobs\/(discover|shortlist)/.test(location.pathname);

  useEffect(() => {
    const handle = setTimeout(() => {
      const params = new URLSearchParams(searchParams);
      if (search) {
        params.set('query', search);
      } else {
        params.delete('query');
      }
      setSearchParams(params, { replace: true });
    }, 300);
    return () => clearTimeout(handle);
  }, [search, searchParams, setSearchParams]);

  // keep local search state in sync when URL query changes elsewhere
  useEffect(() => {
    setSearch(searchParams.get('query') || '');
  }, [searchParams]);

  return (
    <div>
      <JobsNav />
      <header className={styles.header}>
        {isSearchVisible && (
          <input
            type="search"
            placeholder="Search jobs, companies..."
            aria-label="Search jobs and companies"
            className={styles.search}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
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
