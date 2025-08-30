import { useEffect, useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import styles from './AddJobModal.module.css';

interface Props {
  onClose: () => void;
}

export default function AddJobModal({ onClose }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    title: '',
    company: '',
    url: '',
    location: '',
    description: '',
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    const focusable = ref.current?.querySelector<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusable?.focus();
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'Tab') {
        const nodes = ref.current?.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!nodes || nodes.length === 0) return;
        const first = nodes[0];
        const last = nodes[nodes.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      previous?.focus();
    };
  }, [onClose]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const resp = await fetch('/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: form.title,
        company: form.company,
        url: form.url,
        location: form.location || undefined,
        description: form.description || undefined,
      }),
    });
    if (!resp.ok) {
      setError('Failed to save job');
      return;
    }
    queryClient.invalidateQueries({ queryKey: ['jobs'] });
    onClose();
  };

  return (
    <div className={styles.backdrop} role="dialog" aria-modal="true" onClick={onClose}>
      <div className={styles.modal} ref={ref} onClick={(e) => e.stopPropagation()}>
        <h2 id="add-job-title">Add a New Job Post</h2>
        <form onSubmit={handleSubmit} aria-labelledby="add-job-title">
          <label className={styles.field}>
            <span>Job Title</span>
            <input
              name="title"
              placeholder="Job Title"
              value={form.title}
              onChange={handleChange}
              required
            />
          </label>
          <label className={styles.field}>
            <span>URL for Original Posting</span>
            <input
              name="url"
              type="url"
              placeholder="URL for Original Posting"
              value={form.url}
              onChange={handleChange}
              required
            />
          </label>
          <label className={styles.field}>
            <span>Company Name</span>
            <input
              name="company"
              placeholder="Company Name"
              value={form.company}
              onChange={handleChange}
              required
            />
          </label>
          <label className={styles.field}>
            <span>Location</span>
            <input
              name="location"
              placeholder="Location"
              value={form.location}
              onChange={handleChange}
            />
          </label>
          <label className={styles.field}>
            <span>Job Description</span>
            <textarea
              name="description"
              placeholder="Job Description"
              value={form.description}
              onChange={handleChange}
            />
          </label>
          {error && (
            <p role="alert" className={styles.error}>
              {error}
            </p>
          )}
          <div className={styles.actions}>
            <button type="button" onClick={onClose} className={styles.cancel}>
              Cancel
            </button>
            <button type="submit" className={styles.save}>
              Save Job
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
