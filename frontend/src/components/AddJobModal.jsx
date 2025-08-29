import { useState } from 'react';
import toast from 'react-hot-toast';
import styles from './AddJobModal.module.css';

export default function AddJobModal({ onClose, onSaved }) {
  const [form, setForm] = useState({
    title: '',
    company: '',
    url: '',
    location: '',
    description: '',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        toast.success('Job added');
        onSaved?.();
        onClose();
      } else {
        toast.error('Failed to add job');
      }
    } catch (err) {
      toast.error('Failed to add job');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.backdrop} role="dialog" aria-modal="true">
      <div className={styles.modal}>
        <h2>Add Job</h2>
        <form onSubmit={handleSubmit} className={styles.form}>
          <label>
            Job Title
            <input name="title" value={form.title} onChange={handleChange} required />
          </label>
          <label>
            Company
            <input name="company" value={form.company} onChange={handleChange} required />
          </label>
          <label>
            URL
            <input name="url" value={form.url} onChange={handleChange} required />
          </label>
          <label>
            Location
            <input name="location" value={form.location} onChange={handleChange} />
          </label>
          <label>
            Description
            <textarea name="description" value={form.description} onChange={handleChange} />
          </label>
          <div className={styles.actions}>
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" disabled={submitting}>Save</button>
          </div>
        </form>
      </div>
    </div>
  );
}
