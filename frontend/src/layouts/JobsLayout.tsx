import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import AddJobModal from '../components/AddJobModal';
import styles from './JobsLayout.module.css';

export default function JobsLayout() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div>
      <header className={styles.header}>
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
