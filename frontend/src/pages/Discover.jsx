import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import AddJobModal from '../components/AddJobModal';
import styles from './Discover.module.css';

const fetchJobs = async (params) => {
  const res = await fetch(`/api/jobs/unique?${params.toString()}`);
  if (!res.ok) throw new Error('failed');
  return res.json();
};

export default function Discover() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState(searchParams.get('query') || '');
  const [source, setSource] = useState(searchParams.get('source') || '');
  const [since, setSince] = useState(searchParams.get('since') || '');
  const hide = searchParams.get('hide')?.split(',') ?? [];
  const [hideRejected, setHideRejected] = useState(hide.includes('rejected'));
  const [hideBadFit, setHideBadFit] = useState(hide.includes('bad_fit'));
  const queryClient = useQueryClient();

  const page = Number(searchParams.get('page') || 1);

  useEffect(() => {
    const id = setTimeout(() => {
      const next = new URLSearchParams(searchParams);
      if (search) next.set('query', search);
      else next.delete('query');
      next.set('page', '1');
      setSearchParams(next);
    }, 500);
    return () => clearTimeout(id);
  }, [search]);

  useEffect(() => {
    const next = new URLSearchParams(searchParams);
    if (source) next.set('source', source); else next.delete('source');
    if (since) next.set('since', since); else next.delete('since');
    const hides = [];
    if (hideRejected) hides.push('rejected');
    if (hideBadFit) hides.push('bad_fit');
    if (hides.length) next.set('hide', hides.join(','));
    else next.delete('hide');
    next.set('page', '1');
    setSearchParams(next);
  }, [source, since, hideRejected, hideBadFit]);

  const { data, isLoading, isError } = useQuery(
    ['jobs', searchParams.toString()],
    () => fetchJobs(searchParams),
    {
      keepPreviousData: true,
      staleTime: 30000,
      onError: () => toast.error('Failed to load jobs'),
    }
  );

  const handleAnalyze = async (id) => {
    await fetch(`/api/evaluate/job/${id}`, { method: 'POST' });
    toast.success('Evaluation started');
    setTimeout(() => queryClient.invalidateQueries(['jobs']), 1000);
  };

  const nextPage = () => {
    const next = new URLSearchParams(searchParams);
    next.set('page', String(page + 1));
    setSearchParams(next);
  };

  const prevPage = () => {
    const next = new URLSearchParams(searchParams);
    next.set('page', String(page - 1));
    setSearchParams(next);
  };

  return (
    <div className={styles.discover}>
      <div className={styles.toolbar}>
        <input
          type="text"
          placeholder="Search jobs"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search jobs"
        />
        <select value={source} onChange={(e) => setSource(e.target.value)} aria-label="Source">
          <option value="">All Sources</option>
          <option value="LinkedIn">LinkedIn</option>
          <option value="Indeed">Indeed</option>
        </select>
        <select value={since} onChange={(e) => setSince(e.target.value)} aria-label="Since">
          <option value="">Any time</option>
          <option value="24h">Last 24h</option>
          <option value="7d">Last 7d</option>
          <option value="30d">Last 30d</option>
        </select>
        <label>
          <input
            type="checkbox"
            checked={hideRejected}
            onChange={(e) => setHideRejected(e.target.checked)}
          />
          Hide Rejected
        </label>
        <label>
          <input
            type="checkbox"
            checked={hideBadFit}
            onChange={(e) => setHideBadFit(e.target.checked)}
          />
          Hide Bad Fit
        </label>
        <button onClick={() => setShowModal(true)}>Add Job</button>
      </div>
      {isLoading ? (
        <p>Loading...</p>
      ) : isError ? (
        <p>Failed to load jobs</p>
      ) : data?.data?.length === 0 ? (
        <p>
          No jobs yet — click{' '}
          <button onClick={() => setShowModal(true)}>Add Job</button> to get started.
        </p>
      ) : (
        <table className={styles.table}>
          <thead>
            <tr>
              <th scope="col">Job Title</th>
              <th scope="col">Company</th>
              <th scope="col">Source</th>
              <th scope="col">Updated</th>
              <th scope="col">Decision</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((job) => (
              <tr key={job.id}>
                <td>
                  <Link to={`/jobs/${job.id}`}>{job.title}</Link>
                </td>
                <td>{job.company}</td>
                <td>{job.source}</td>
                <td>{new Date(job.updated_at).toLocaleString()}</td>
                <td>
                  <span className={styles.decision}>{job.decision}</span>
                </td>
                <td>
                  <button onClick={() => handleAnalyze(job.id)}>Analyze</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {data?.meta && (
        <div className={styles.pagination}>
          <button onClick={prevPage} disabled={page <= 1}>
            Prev
          </button>
          <span>Page {page}</span>
          <button onClick={nextPage} disabled={page >= data.meta.page_count}>
            Next
          </button>
        </div>
      )}
      {showModal && (
        <AddJobModal
          onClose={() => setShowModal(false)}
          onSaved={() => queryClient.invalidateQueries(['jobs'])}
        />
      )}
    </div>
  );
}
