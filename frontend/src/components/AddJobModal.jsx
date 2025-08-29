import styles from './AddJobModal.module.css';

export default function AddJobModal({ onClose }) {
  return (
    <div className={styles.backdrop} role="dialog" aria-modal="true">
      <div className={styles.modal}>
        <h2>Add Job</h2>
        <p>Job form goes here.</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
