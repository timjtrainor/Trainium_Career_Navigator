@@ .. @@
-import { Link, useLocation, useSearchParams } from 'react-router-dom';
+import { useLocation, useSearchParams } from 'react-router-dom';
 import { useQuery, useQueryClient } from '@tanstack/react-query';
 import { useState } from 'react';
+import { Briefcase, Grid, List } from 'lucide-react';
+import JobCard from '../components/JobCard';
+import FilterPanel from '../components/FilterPanel';
+import EmptyState from '../components/EmptyState';
+import LoadingSpinner from '../components/LoadingSpinner';
+import Pagination from '../components/Pagination';
 import Toast from '../components/Toast';
-import styles from './JobsDiscoverPage.module.css';
 
 interface Job {
@@ .. @@
   meta: { page: number; page_count: number; total: number };
 }
 
-function formatRelative(value?: string) {
-  if (!value) return '';
-  const date = new Date(value);
-  const diff = Date.now() - date.getTime();
-  const minutes = Math.floor(diff / 60000);
-  if (minutes < 60) return `${minutes}m ago`;
-  const hours = Math.floor(minutes / 60);
-  if (hours < 24) return `${hours}h ago`;
-  const days = Math.floor(hours / 24);
-  return `${days}d ago`;
-}
-
 export default function JobsDiscoverPage() {
-  const location = useLocation();
   const queryClient = useQueryClient();
-  const [searchParams, setSearchParams] = useSearchParams();
+  const [searchParams, setSearchParams] = useSearchParams();
+  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
   const [toast, setToast] = useState('');
 
@@ .. @@
   const selectedSources = searchParams.getAll('source');
   const hide = searchParams.get('hide') === '1';
 
@@ .. @@
     staleTime: 30000,
   });
 
@@ .. @@
   const updateParams = (
     updates: Record<string, string | string[] | null>
   ) => {
@@ .. @@
     setSearchParams(next, { replace: true });
   };
 
+  const resetFilters = () => {
+    setSearchParams(new URLSearchParams(), { replace: true });
+  };
+
   const handleAnalyze = async (id: string) => {
@@ .. @@
     setToast('Evaluation started');
     setTimeout(() => {
       queryClient.invalidateQueries({ queryKey: ['jobs'] });
     }, 1000);
   };
 
-  const onPage = (p: number) => updateParams({ page: String(p) });
+  const handlePageChange = (p: number) => updateParams({ page: String(p) });
 
   return (
-    <div>
-      <h1>Discover Jobs</h1>
-      <div className={styles.filters}>
-        <label>
-          Source
-          <select
-            multiple
-            value={selectedSources}
-            onChange={(e) => {
-              const opts = Array.from(e.target.selectedOptions).map((o) => o.value);
-              updateParams({ source: opts });
-            }}
-          >
-            {sources.map((s) => (
-              <option key={s} value={s}>
-                {s}
-              </option>
-            ))}
-          </select>
-        </label>
-        <label>
-          Since
-          <select
-            value={since}
-            onChange={(e) => updateParams({ since: e.target.value || null })}
-          >
-            <option value="">Any time</option>
-            <option value="24h">Last 24h</option>
-            <option value="7d">Last 7d</option>
-            <option value="30d">Last 30d</option>
-          </select>
-        </label>
-        <label>
-          <input
-            type="checkbox"
-            checked={hide}
-            onChange={() => updateParams({ hide: hide ? null : '1' })}
-          />{' '}
-          Hide Rejected/Bad Fit
-        </label>
+    <div className="space-y-6">
+      {/* Stats Bar */}
+      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-gray-900">{data?.meta.total || 0}</div>
+            <div className="text-sm text-gray-500">Total Jobs</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-primary-600">
+              {data?.data.filter(j => j.decision === 'recommended').length || 0}
+            </div>
+            <div className="text-sm text-gray-500">Recommended</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-warning-600">
+              {data?.data.filter(j => j.decision === 'pending' || j.decision === 'evaluating').length || 0}
+            </div>
+            <div className="text-sm text-gray-500">Pending Review</div>
+          </div>
+        </div>
       </div>
-      {isLoading && <p>Loading...</p>}
-      {error && <p role="alert">Error loading jobs</p>}
-      {!isLoading && data && data.data.length === 0 && (
-        <p>No jobs yet — click Add Job to get started.</p>
-      )}
-      {data && data.data.length > 0 && (
-        <table className={styles.table}>
-          <thead>
-            <tr>
-              <th scope="col">Job Title</th>
-              <th scope="col">Company</th>
-              <th scope="col">Source</th>
-              <th scope="col">Updated</th>
-              <th scope="col">Decision</th>
-              <th scope="col">Actions</th>
-            </tr>
-          </thead>
-          <tbody>
-            {data.data.map((job) => (
-              <tr key={job.id}>
-                <td>
-                  <Link
-                    to={`/jobs/${job.id}`}
-                    state={{ backgroundLocation: location }}
-                  >
-                    {job.title}
-                  </Link>
-                </td>
-                <td>{job.company}</td>
-                <td>{job.source}</td>
-                <td>{formatRelative(job.updated_at)}</td>
-                <td>
-                  {job.decision && (
-                    <span className={styles.pill}>{job.decision}</span>
-                  )}
-                </td>
-                <td className={styles.actions}>
-                  <button onClick={() => handleAnalyze(job.id)}>Analyze</button>
-                </td>
-              </tr>
-            ))}
-          </tbody>
-        </table>
-      )}
-      {data && data.meta.page_count > 1 && (
-        <nav className={styles.pagination} aria-label="Pagination">
-          <button onClick={() => onPage(page - 1)} disabled={page <= 1}>
-            Previous
-          </button>
-          <span>
-            Page {data.meta.page} of {data.meta.page_count}
-          </span>
-          <button
-            onClick={() => onPage(page + 1)}
-            disabled={page >= data.meta.page_count}
-          >
-            Next
-          </button>
-        </nav>
-      )}
-      {toast && <Toast message={toast} onDismiss={() => setToast('')} />}
+
+      <div className="flex flex-col lg:flex-row gap-6">
+        {/* Filters Sidebar */}
+        <div className="lg:w-64 flex-shrink-0">
+          <FilterPanel
+            sources={sources}
+            selectedSources={selectedSources}
+            onSourcesChange={(sources) => updateParams({ source: sources })}
+            since={since}
+            onSinceChange={(since) => updateParams({ since: since || null })}
+            hideRejected={hide}
+            onHideRejectedChange={(hide) => updateParams({ hide: hide ? '1' : null })}
+            onReset={resetFilters}
+          />
+        </div>

+        {/* Main Content */}
+        <div className="flex-1 min-w-0">
+          {/* View Toggle */}
+          <div className="flex items-center justify-between mb-6">
+            <div className="flex items-center space-x-2">
+              <span className="text-sm text-gray-500">View:</span>
+              <div className="flex rounded-lg border border-gray-300 overflow-hidden">
+                <button
+                  onClick={() => setViewMode('grid')}
+                  className={`
+                    px-3 py-1 text-sm transition-colors
+                    ${viewMode === 'grid' 
+                      ? 'bg-primary-600 text-white' 
+                      : 'bg-white text-gray-700 hover:bg-gray-50'
+                    }
+                  `}
+                >
+                  <Grid className="w-4 h-4" />
+                </button>
+                <button
+                  onClick={() => setViewMode('table')}
+                  className={`
+                    px-3 py-1 text-sm transition-colors border-l border-gray-300
+                    ${viewMode === 'table' 
+                      ? 'bg-primary-600 text-white' 
+                      : 'bg-white text-gray-700 hover:bg-gray-50'
+                    }
+                  `}
+                >
+                  <List className="w-4 h-4" />
+                </button>
+              </div>
+            </div>
+            
+            {data && (
+              <p className="text-sm text-gray-500">
+                {data.meta.total} jobs found
+              </p>
+            )}
+          </div>

+          {/* Loading State */}
+          {isLoading && (
+            <div className="flex items-center justify-center py-12">
+              <LoadingSpinner size="lg" />
+            </div>
+          )}

+          {/* Error State */}
+          {error && (
+            <div className="card bg-error-50 border-error-200">
+              <p className="text-error-700 text-center">Failed to load jobs. Please try again.</p>
+            </div>
+          )}

+          {/* Empty State */}
+          {!isLoading && data && data.data.length === 0 && (
+            <EmptyState
+              icon={<Briefcase className="w-12 h-12" />}
+              title="No jobs found"
+              description="Try adjusting your filters or add a job manually to get started."
+              action={
+                <button 
+                  onClick={() => setShowAddJobModal(true)}
+                  className="btn-primary"
+                >
+                  Add Your First Job
+                </button>
+              }
+            />
+          )}

+          {/* Jobs Grid/Table */}
+          {data && data.data.length > 0 && (
+            <>
+              {viewMode === 'grid' ? (
+                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
+                  {data.data.map((job) => (
+                    <JobCard
+                      key={job.id}
+                      job={job}
+                      onAnalyze={handleAnalyze}
+                    />
+                  ))}
+                </div>
+              ) : (
+                <div className="card overflow-hidden">
+                  <div className="overflow-x-auto">
+                    <table className="min-w-full divide-y divide-gray-200">
+                      <thead className="bg-gray-50">
+                        <tr>
+                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Job
+                          </th>
+                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Company
+                          </th>
+                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Source
+                          </th>
+                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Updated
+                          </th>
+                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Status
+                          </th>
+                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
+                            Actions
+                          </th>
+                        </tr>
+                      </thead>
+                      <tbody className="bg-white divide-y divide-gray-200">
+                        {data.data.map((job) => (
+                          <tr key={job.id} className="hover:bg-gray-50">
+                            <td className="px-6 py-4">
+                              <Link
+                                to={`/jobs/${job.id}`}
+                                state={{ backgroundLocation: location }}
+                                className="text-primary-600 hover:text-primary-800 font-medium"
+                              >
+                                {job.title || 'Untitled Position'}
+                              </Link>
+                            </td>
+                            <td className="px-6 py-4 text-sm text-gray-900">
+                              {job.company || '—'}
+                            </td>
+                            <td className="px-6 py-4 text-sm text-gray-500 capitalize">
+                              {job.source || '—'}
+                            </td>
+                            <td className="px-6 py-4 text-sm text-gray-500">
+                              {job.updated_at ? new Date(job.updated_at).toLocaleDateString() : '—'}
+                            </td>
+                            <td className="px-6 py-4">
+                              {job.decision ? (
+                                <DecisionPill decision={job.decision} />
+                              ) : (
+                                <span className="text-sm text-gray-400">—</span>
+                              )}
+                            </td>
+                            <td className="px-6 py-4 text-right">
+                              <button
+                                onClick={() => handleAnalyze(job.id)}
+                                className="btn-ghost text-sm"
+                              >
+                                Analyze
+                              </button>
+                            </td>
+                          </tr>
+                        ))}
+                      </tbody>
+                    </table>
+                  </div>
+                </div>
+              )}

+              {/* Pagination */}
+              {data.meta.page_count > 1 && (
+                <div className="mt-6">
+                  <Pagination
+                    currentPage={page}
+                    totalPages={data.meta.page_count}
+                    onPageChange={handlePageChange}
+                  />
+                </div>
+              )}
+            </>
+          )}
+        </div>
+      </div>
+
+      {toast && (
+        <Toast 
+          message={toast} 
+          type="success"
+          onDismiss={() => setToast('')} 
+        />
+      )}
     </div>
   );
 }