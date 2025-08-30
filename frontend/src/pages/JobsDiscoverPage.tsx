import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useState } from 'react';
import Toast from '../components/Toast';
import styles from './JobsDiscoverPage.module.css';

interface Job {
  id: string;
  title?: string;
  company?: string;
  source?: string;
  updated_at?: string;
  decision?: string;
}

interface JobListResponse {
  data: Job[];
  meta: { page: number; page_count: number; total: number };
}

function formatRelative(value?: string) {
  if (!value) return '';
  const date = new Date(value);
  const diff = Date.now() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function JobsDiscoverPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [searchParams, setSearchParams] = useSearchParams();
  const [toast, setToast] = useState('');

  const page = Number(searchParams.get('page') || 1);
  const query = searchParams.get('query') || '';
  const since = searchParams.get('since') || '';
  const selectedSources = searchParams.getAll('source');
  const hide = searchParams.get('hide') === '1';

  const params = new URLSearchParams();
  if (query) params.set('query', query);
  selectedSources.forEach((s) => params.append('source', s));
  if (since) params.set('since', since);
  if (hide) {
    params.append('hide', 'rejected');
    params.append('hide', 'bad_fit');
  }
  params.set('page', String(page));

  const { data, isLoading, error } = useQuery<JobListResponse>({
    queryKey: ['jobs', params.toString()],
    queryFn: async () => {
      const resp = await fetch(`/api/jobs/unique?${params.toString()}`);
      if (!resp.ok) throw new Error('failed');
      return resp.json();
    },
    keepPreviousData: true,
    staleTime: 30000,
  });

  const sources = Array.from(
    new Set((data?.data || []).map((j) => j.source).filter(Boolean))
  ) as string[];

  const updateParams = (
    updates: Record<string, string | string[] | null>
  ) => {
    const next = new URLSearchParams(searchParams);
    Object.entries(updates).forEach(([k, v]) => {
      next.delete(k);
      if (Array.isArray(v)) v.forEach((item) => next.append(k, item));
      else if (v) next.set(k, v);
    });
    if (updates.page === undefined) next.set('page', '1');
    setSearchParams(next, { replace: true });
  };

  const handleAnalyze = async (id: string) => {
    await fetch(`/api/evaluate/job/${id}`, { method: 'POST' });
    setToast('Evaluation started');
    setTimeout(() => {
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    }, 1000);
  };

  const onPage = (p: number) => updateParams({ page: String(p) });

  return (
    <div>
      <h1>Discover Jobs</h1>
      <div className={styles.filters}>
        <label>
          Source
          <select
            multiple
            value={selectedSources}
            onChange={(e) => {
              const opts = Array.from(e.target.selectedOptions).map((o) => o.value);
              updateParams({ source: opts });
            }}
          >
            {sources.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </label>
        <label>
          Since
          <select
            value={since}
            onChange={(e) => updateParams({ since: e.target.value || null })}
          >
            <option value="">Any time</option>
            <option value="24h">Last 24h</option>
            <option value="7d">Last 7d</option>
            <option value="30d">Last 30d</option>
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={hide}
            onChange={() => updateParams({ hide: hide ? null : '1' })}
          />{' '}
          Hide Rejected/Bad Fit
        </label>
      </div>
      {isLoading && <p>Loading...</p>}
      {error && <p role="alert">Error loading jobs</p>}
      {!isLoading && data && data.data.length === 0 && (
        <p>No jobs yet — click Add Job to get started.</p>
      )}
      {data && data.data.length > 0 && (
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
                  <Link
                    to={`/jobs/${job.id}`}
                    state={{ backgroundLocation: location }}
                  >
                    {job.title}
                  </Link>
                </td>
                <td>{job.company}</td>
                <td>{job.source}</td>
                <td>{formatRelative(job.updated_at)}</td>
                <td>
                  {job.decision && (
                    <span className={styles.pill}>{job.decision}</span>
                  )}
                </td>
                <td className={styles.actions}>
                  <button onClick={() => handleAnalyze(job.id)}>Analyze</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {data && data.meta.page_count > 1 && (
        <nav className={styles.pagination} aria-label="Pagination">
          <button onClick={() => onPage(page - 1)} disabled={page <= 1}>
            Previous
          </button>
          <span>
            Page {data.meta.page} of {data.meta.page_count}
          </span>
          <button
            onClick={() => onPage(page + 1)}
            disabled={page >= data.meta.page_count}
          >
            Next
          </button>
        </nav>
      )}
      {toast && <Toast message={toast} onDismiss={() => setToast('')} />}
    </div>
  );
}
