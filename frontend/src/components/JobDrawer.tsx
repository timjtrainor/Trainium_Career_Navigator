import { useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import styles from './JobDrawer.module.css';

export default function JobDrawer() {
  const { id } = useParams();
  const navigate = useNavigate();
  const ref = useRef<HTMLDivElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const onClose = () => navigate(-1);
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    closeButtonRef.current?.focus();
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        const focusable = ref.current?.querySelectorAll<HTMLElement>('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (!focusable || focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      }
    }
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      prev?.focus();
    };
  }, []);
  return (
    <div className={styles.backdrop} role="dialog" aria-modal="true">
      <div className={styles.drawer} ref={ref}>
        <h2>Job Detail {id}</h2>
        <button ref={closeButtonRef} onClick={onClose} className={styles.closeButton}>Close</button>
      </div>
    </div>
  );
}
