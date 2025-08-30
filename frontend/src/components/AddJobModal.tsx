import { useEffect, useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import styles from './AddJobModal.module.css';

interface Props {
  onClose: () => void;
  onSuccess: (msg: string) => void;
}

export default function AddJobModal({ onClose, onSuccess }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    title: '',
    company: '',
    url: '',
    location: '',
    description: '',
    salary: '',
    job_type: '',
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const mutation = useMutation({
    mutationFn: async () => {
      const resp = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: form.title,
          company: form.company,
          url: form.url,
          location: form.location,
          description: form.description,
          salary: form.salary || undefined,
          job_type: form.job_type || undefined,
        }),
      });
      if (!resp.ok) throw new Error('failed');
      return resp.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      onSuccess('Job saved');
      onClose();
    },
    onError: () => setError('Failed to save job'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!form.description.trim()) {
      setError('Description is required');
      return;
    }
    mutation.mutate();
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
              required
            />
          </label>
          <label className={styles.field}>
            <span>Job Description</span>
            <div
              className={styles.rich}
              contentEditable
              role="textbox"
              aria-multiline="true"
              onInput={(e) =>
                setForm({ ...form, description: (e.target as HTMLDivElement).innerHTML })
              }
            />
          </label>
          <label className={styles.field}>
            <span>Salary Range</span>
            <input
              name="salary"
              placeholder="e.g. 100k-120k"
              value={form.salary}
              onChange={handleChange}
            />
          </label>
          <label className={styles.field}>
            <span>Job Type</span>
            <input
              name="job_type"
              placeholder="e.g. full-time"
              value={form.job_type}
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
            <button type="submit" className={styles.save} disabled={mutation.isLoading}>
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
