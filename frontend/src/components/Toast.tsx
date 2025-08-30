import { useEffect } from 'react';
import styles from './Toast.module.css';

interface Props {
  message: string;
  onDismiss: () => void;
}

export default function Toast({ message, onDismiss }: Props) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <div className={styles.toast} role="status" aria-live="polite">
      {message}
    </div>
  );
}
