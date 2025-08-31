import { useEffect, useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import styles from './AddJobModal.module.css';

interface Props {
  onClose: () => void;
  onSuccess?: (message: string) => void;
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
    salary_min: '',
    salary_max: '',
    job_type: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    // Basic validation
    if (form.salary_min && form.salary_max && parseInt(form.salary_min) > parseInt(form.salary_max)) {
      setError('Minimum salary cannot be greater than maximum salary');
      setIsSubmitting(false);
      return;
    }

    try {
      const resp = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: form.title,
          company: form.company,
          url: form.url,
          location: form.location || undefined,
          description: form.description || undefined,
          salary_min: form.salary_min ? parseInt(form.salary_min) : undefined,
          salary_max: form.salary_max ? parseInt(form.salary_max) : undefined,
          job_type: form.job_type || undefined,
        }),
      });
      
      if (!resp.ok) {
        const errorData = await resp.json().catch(() => ({}));
        setError(errorData.detail || 'Failed to save job');
        return;
      }
      
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      onSuccess?.('Job posting created successfully!');
      onClose();
    } catch (error) {
      setError('Network error. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
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
          <label className={styles.field}>
            <span>Salary Range</span>
            <div className={styles.salaryRange}>
              <input
                name="salary_min"
                type="number"
                placeholder="Min Salary"
                value={form.salary_min}
                onChange={handleChange}
                min="0"
              />
              <span>to</span>
              <input
                name="salary_max"
                type="number"
                placeholder="Max Salary"
                value={form.salary_max}
                onChange={handleChange}
                min="0"
              />
            </div>
          </label>
          <label className={styles.field}>
            <span>Job Type</span>
            <select
              name="job_type"
              value={form.job_type}
              onChange={handleChange}
            >
              <option value="">Select Job Type</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
              <option value="Freelance">Freelance</option>
            </select>
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
            <button type="submit" className={styles.save} disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : 'Save Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
