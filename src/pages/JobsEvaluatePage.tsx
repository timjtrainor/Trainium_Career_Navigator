@@ .. @@
+import { useState } from 'react';
+import { useQuery } from '@tanstack/react-query';
+import { Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
+import JobCard from '../components/JobCard';
+import EmptyState from '../components/EmptyState';
+import LoadingSpinner from '../components/LoadingSpinner';
+import DecisionPill from '../components/DecisionPill';
+
+interface Job {
+  id: string;
+  title?: string;
+  company?: string;
+  source?: string;
+  updated_at?: string;
+  decision?: string;
+}
+
+interface JobListResponse {
+  data: Job[];
+  meta: { page: number; page_count: number; total: number };
+}
+
 export default function JobsEvaluatePage() {
-  return <h1>Evaluate Jobs</h1>;
+  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
+
+  const { data, isLoading, error } = useQuery<JobListResponse>({
+    queryKey: ['jobs', 'evaluate', filter],
+    queryFn: async () => {
+      const params = new URLSearchParams();
+      if (filter === 'pending') {
+        params.append('hide', 'recommended');
+        params.append('hide', 'rejected');
+        params.append('hide', 'bad_fit');
+      } else if (filter === 'completed') {
+        params.append('hide', 'undecided');
+        params.append('hide', 'pending');
+        params.append('hide', 'evaluating');
+      }
+      
+      const resp = await fetch(`/api/jobs/unique?${params.toString()}`);
+      if (!resp.ok) throw new Error('failed');
+      return resp.json();
+    },
+    staleTime: 30000,
+  });
+
+  const stats = {
+    pending: data?.data.filter(j => ['undecided', 'pending', 'evaluating'].includes(j.decision || '')).length || 0,
+    recommended: data?.data.filter(j => j.decision === 'recommended').length || 0,
+    rejected: data?.data.filter(j => ['rejected', 'bad_fit'].includes(j.decision || '')).length || 0,
+  };
+
+  return (
+    <div className="space-y-6">
+      {/* Stats Overview */}
+      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-warning-100 rounded-lg">
+              <Clock className="w-6 h-6 text-warning-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.pending}</div>
+              <div className="text-sm text-gray-500">Pending Evaluation</div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-success-100 rounded-lg">
+              <CheckCircle className="w-6 h-6 text-success-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.recommended}</div>
+              <div className="text-sm text-gray-500">Recommended</div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-error-100 rounded-lg">
+              <XCircle className="w-6 h-6 text-error-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.rejected}</div>
+              <div className="text-sm text-gray-500">Not Recommended</div>
+            </div>
+          </div>
+        </div>
+      </div>

+      {/* Filter Tabs */}
+      <div className="card">
+        <div className="flex space-x-1 p-1 bg-gray-100 rounded-lg">
+          {[
+            { key: 'all', label: 'All Jobs', count: data?.meta.total || 0 },
+            { key: 'pending', label: 'Pending', count: stats.pending },
+            { key: 'completed', label: 'Completed', count: stats.recommended + stats.rejected },
+          ].map((tab) => (
+            <button
+              key={tab.key}
+              onClick={() => setFilter(tab.key as any)}
+              className={`
+                flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors
+                ${filter === tab.key
+                  ? 'bg-white text-gray-900 shadow-sm'
+                  : 'text-gray-600 hover:text-gray-900'
+                }
+              `}
+            >
+              {tab.label} ({tab.count})
+            </button>
+          ))}
+        </div>
+      </div>

+      {/* Loading State */}
+      {isLoading && (
+        <div className="flex items-center justify-center py-12">
+          <LoadingSpinner size="lg" />
+        </div>
+      )}

+      {/* Error State */}
+      {error && (
+        <div className="card bg-error-50 border-error-200">
+          <div className="flex items-center space-x-2">
+            <AlertCircle className="w-5 h-5 text-error-600" />
+            <p className="text-error-700">Failed to load evaluations. Please try again.</p>
+          </div>
+        </div>
+      )}

+      {/* Empty State */}
+      {!isLoading && data && data.data.length === 0 && (
+        <EmptyState
+          icon={<Clock className="w-12 h-12" />}
+          title="No evaluations found"
+          description="Jobs will appear here once they've been analyzed by our AI personas."
+        />
+      )}

+      {/* Jobs List */}
+      {data && data.data.length > 0 && (
+        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
+          {data.data.map((job) => (
+            <JobCard
+              key={job.id}
+              job={job}
+              onAnalyze={async (id) => {
+                await fetch(`/api/evaluate/job/${id}`, { method: 'POST' });
+                // Refresh data after a short delay
+                setTimeout(() => {
+                  // queryClient.invalidateQueries({ queryKey: ['jobs'] });
+                }, 1000);
+              }}
+            />
+          ))}
+        </div>
+      )}
+    </div>
+  );
 }