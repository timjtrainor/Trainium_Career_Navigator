@@ .. @@
-import { useParams } from 'react-router-dom';
+import { useParams, useNavigate } from 'react-router-dom';
+import { useQuery } from '@tanstack/react-query';
+import { ArrowLeft, ExternalLink, RotateCcw } from 'lucide-react';
+import DecisionPill from '../components/DecisionPill';
+import LoadingSpinner from '../components/LoadingSpinner';
+
+interface JobDetail {
+  job_id: string;
+  title?: string;
+  company?: string;
+  description?: string;
+  location?: string;
+  url?: string;
+  source?: string;
+  updated_at?: string;
+  evaluation: {
+    yes: number;
+    no: number;
+    final_decision_bool?: boolean;
+    confidence?: number;
+  };
+}
 
 export default function JobDetailPage() {
   const { id } = useParams();
+  const navigate = useNavigate();
+
+  const { data: job, isLoading, error } = useQuery<JobDetail>({
+    queryKey: ['job', id],
+    queryFn: async () => {
+      const resp = await fetch(`/api/jobs/${id}`);
+      if (!resp.ok) throw new Error('Failed to fetch job');
+      return resp.json();
+    },
+    enabled: !!id,
+  });
+
+  if (isLoading) {
+    return (
+      <div className="flex items-center justify-center py-12">
+        <LoadingSpinner size="lg" />
+      </div>
+    );
+  }
+
+  if (error || !job) {
+    return (
+      <div className="card bg-error-50 border-error-200">
+        <p className="text-error-700 text-center">Job not found or failed to load.</p>
+      </div>
+    );
+  }
+
   return (
-    <main id="main">
-      <h1>Job Detail {id}</h1>
-    </main>
+    <div className="space-y-6">
+      {/* Back Button */}
+      <button
+        onClick={() => navigate(-1)}
+        className="btn-ghost flex items-center space-x-2"
+      >
+        <ArrowLeft className="w-4 h-4" />
+        <span>Back</span>
+      </button>

+      {/* Job Header */}
+      <div className="card">
+        <div className="flex items-start justify-between mb-6">
+          <div className="flex-1">
+            <h1 className="text-3xl font-bold text-gray-900 mb-2">
+              {job.title || 'Untitled Position'}
+            </h1>
+            <p className="text-xl text-gray-600 mb-2">{job.company}</p>
+            {job.location && (
+              <p className="text-gray-500">{job.location}</p>
+            )}
+          </div>
+          <div className="flex items-center space-x-3">
+            {job.evaluation.final_decision_bool !== undefined && (
+              <DecisionPill 
+                decision={job.evaluation.final_decision_bool ? 'recommended' : 'rejected'} 
+                size="md"
+              />
+            )}
+            {job.url && (
+              <a
+                href={job.url}
+                target="_blank"
+                rel="noopener noreferrer"
+                className="btn-primary flex items-center space-x-2"
+              >
+                <span>View Original</span>
+                <ExternalLink className="w-4 h-4" />
+              </a>
+            )}
+          </div>
+        </div>

+        {/* Evaluation Summary */}
+        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
+          <div className="bg-success-50 border border-success-200 rounded-lg p-4 text-center">
+            <div className="text-2xl font-bold text-success-700">{job.evaluation.yes}</div>
+            <div className="text-sm text-success-600">Positive Reviews</div>
+          </div>
+          <div className="bg-error-50 border border-error-200 rounded-lg p-4 text-center">
+            <div className="text-2xl font-bold text-error-700">{job.evaluation.no}</div>
+            <div className="text-sm text-error-600">Negative Reviews</div>
+          </div>
+          <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 text-center">
+            <div className="text-2xl font-bold text-primary-700">
+              {job.evaluation.confidence ? Math.round(job.evaluation.confidence * 100) : '—'}%
+            </div>
+            <div className="text-sm text-primary-600">Confidence</div>
+          </div>
+        </div>

+        <button className="btn-secondary flex items-center space-x-2">
+          <RotateCcw className="w-4 h-4" />
+          <span>Re-analyze Job</span>
+        </button>
+      </div>

+      {/* Job Description */}
+      {job.description && (
+        <div className="card">
+          <h2 className="text-lg font-semibold text-gray-900 mb-4">Job Description</h2>
+          <div className="prose prose-sm max-w-none">
+            <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
+          </div>
+        </div>
+      )}

+      {/* Metadata */}
+      <div className="card">
+        <h2 className="text-lg font-semibold text-gray-900 mb-4">Job Information</h2>
+        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
+          <div>
+            <dt className="text-sm font-medium text-gray-500">Source</dt>
+            <dd className="text-sm text-gray-900 capitalize">{job.source || 'Unknown'}</dd>
+          </div>
+          <div>
+            <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
+            <dd className="text-sm text-gray-900">
+              {job.updated_at ? new Date(job.updated_at).toLocaleDateString() : 'Unknown'}
+            </dd>
+          </div>
+          <div>
+            <dt className="text-sm font-medium text-gray-500">Job ID</dt>
+            <dd className="text-sm text-gray-900 font-mono">{job.job_id}</dd>
+          </div>
+        </dl>
+      </div>
+    </div>
   );
 }