import { Outlet } from 'react-router-dom';
import styles from './JobsLayout.module.css';

export default function JobsLayout() {
  return (
    <main id="main" className={styles.main}>
      <Outlet />
    </main>
  );
}
