@@ .. @@
-import { useEffect, useRef } from 'react';
+import { useEffect, useRef, useState } from 'react';
 import { useNavigate, useParams } from 'react-router-dom';
-import styles from './JobDrawer.module.css';
+import { useQuery } from '@tanstack/react-query';
+import { X, ExternalLink, ThumbsUp, ThumbsDown, RotateCcw } from 'lucide-react';
+import DecisionPill from './DecisionPill';
+import LoadingSpinner from './LoadingSpinner';
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
 
 export default function JobDrawer() {
   const { id } = useParams();
   const navigate = useNavigate();
   const ref = useRef<HTMLDivElement>(null);
+  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);
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
 
   useEffect(() => {
@@ .. @@
     };
   }, [navigate]);
 
-  const onClose = () => navigate(-1);
+  const onClose = () => navigate(-1);
+
+  const handleAnalyze = async () => {
+    if (!id) return;
+    await fetch(`/api/evaluate/job/${id}`, { method: 'POST' });
+    // Could show toast or refresh data
+  };
+
+  const handleFeedback = async (vote: 'up' | 'down') => {
+    setFeedback(vote);
+    // In a real app, this would submit feedback to the API
+  };
 
   return (
-    <div className={styles.backdrop} role="dialog" aria-modal="true" onClick={onClose}>
-      <div className={styles.drawer} ref={ref} onClick={(e) => e.stopPropagation()}>
-        <h2>Job Detail {id}</h2>
-        <button onClick={onClose}>Close</button>
+    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 animate-fade-in" role="dialog" aria-modal="true" onClick={onClose}>
+      <div 
+        ref={ref} 
+        className="fixed top-0 right-0 w-full max-w-2xl h-full bg-white shadow-xl animate-slide-in overflow-y-auto"
+        onClick={(e) => e.stopPropagation()}
+      >
+        {/* Header */}
+        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 z-10">
+          <div className="flex items-center justify-between">
+            <h2 className="text-lg font-semibold text-gray-900">Job Details</h2>
+            <button
+              onClick={onClose}
+              className="p-2 rounded-md hover:bg-gray-100 transition-colors"
+              aria-label="Close drawer"
+            >
+              <X className="w-5 h-5" />
+            </button>
+          </div>
+        </div>
+
+        {/* Content */}
+        <div className="p-6">
+          {isLoading && (
+            <div className="flex items-center justify-center py-12">
+              <LoadingSpinner size="lg" />
+            </div>
+          )}
+
+          {error && (
+            <div className="text-center py-12">
+              <p className="text-error-600">Failed to load job details</p>
+            </div>
+          )}
+
+          {job && (
+            <div className="space-y-6">
+              {/* Job Header */}
+              <div>
+                <div className="flex items-start justify-between mb-4">
+                  <div>
+                    <h1 className="text-2xl font-bold text-gray-900 mb-2">
+                      {job.title || 'Untitled Position'}
+                    </h1>
+                    <p className="text-lg text-gray-600">{job.company}</p>
+                    {job.location && (
+                      <p className="text-sm text-gray-500">{job.location}</p>
+                    )}
+                  </div>
+                  {job.url && (
+                    <a
+                      href={job.url}
+                      target="_blank"
+                      rel="noopener noreferrer"
+                      className="btn-secondary flex items-center space-x-2"
+                    >
+                      <span>View Original</span>
+                      <ExternalLink className="w-4 h-4" />
+                    </a>
+                  )}
+                </div>

+                {/* Decision Summary */}
+                {job.evaluation.final_decision_bool !== undefined && (
+                  <div className="card bg-gray-50">
+                    <div className="flex items-center justify-between">
+                      <div>
+                        <h3 className="font-medium text-gray-900 mb-1">Final Recommendation</h3>
+                        <div className="flex items-center space-x-3">
+                          <DecisionPill 
+                            decision={job.evaluation.final_decision_bool ? 'recommended' : 'rejected'} 
+                            size="md"
+                          />
+                          {job.evaluation.confidence && (
+                            <span className="text-sm text-gray-600">
+                              {Math.round(job.evaluation.confidence * 100)}% confidence
+                            </span>
+                          )}
+                        </div>
+                      </div>
+                      <button
+                        onClick={handleAnalyze}
+                        className="btn-ghost flex items-center space-x-2"
+                      >
+                        <RotateCcw className="w-4 h-4" />
+                        <span>Re-analyze</span>
+                      </button>
+                    </div>
+                  </div>
+                )}
+              </div>

+              {/* Evaluation Summary */}
+              <div>
+                <h3 className="font-medium text-gray-900 mb-3">Evaluation Summary</h3>
+                <div className="grid grid-cols-2 gap-4">
+                  <div className="card bg-success-50 border-success-200">
+                    <div className="text-center">
+                      <div className="text-2xl font-bold text-success-700">{job.evaluation.yes}</div>
+                      <div className="text-sm text-success-600">Positive Reviews</div>
+                    </div>
+                  </div>
+                  <div className="card bg-error-50 border-error-200">
+                    <div className="text-center">
+                      <div className="text-2xl font-bold text-error-700">{job.evaluation.no}</div>
+                      <div className="text-sm text-error-600">Negative Reviews</div>
+                    </div>
+                  </div>
+                </div>
+              </div>

+              {/* Description */}
+              {job.description && (
+                <div>
+                  <h3 className="font-medium text-gray-900 mb-3">Job Description</h3>
+                  <div className="card bg-gray-50">
+                    <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
+                  </div>
+                </div>
+              )}

+              {/* Feedback */}
+              <div>
+                <h3 className="font-medium text-gray-900 mb-3">Your Feedback</h3>
+                <div className="flex items-center space-x-4">
+                  <button
+                    onClick={() => handleFeedback('up')}
+                    className={`
+                      flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors
+                      ${feedback === 'up'
+                        ? 'bg-success-50 border-success-300 text-success-700'
+                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
+                      }
+                    `}
+                  >
+                    <ThumbsUp className="w-4 h-4" />
+                    <span>Helpful</span>
+                  </button>
+                  <button
+                    onClick={() => handleFeedback('down')}
+                    className={`
+                      flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors
+                      ${feedback === 'down'
+                        ? 'bg-error-50 border-error-300 text-error-700'
+                        : 'border-gray-300 text-gray-700 hover:bg-gray-50'
+                      }
+                    `}
+                  >
+                    <ThumbsDown className="w-4 h-4" />
+                    <span>Not Helpful</span>
+                  </button>
+                </div>
+              </div>

+              {/* Metadata */}
+              <div className="border-t border-gray-200 pt-6">
+                <h3 className="font-medium text-gray-900 mb-3">Job Metadata</h3>
+                <dl className="grid grid-cols-1 gap-3 sm:grid-cols-2">
+                  <div>
+                    <dt className="text-sm font-medium text-gray-500">Source</dt>
+                    <dd className="text-sm text-gray-900 capitalize">{job.source || 'Unknown'}</dd>
+                  </div>
+                  <div>
+                    <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
+                    <dd className="text-sm text-gray-900">
+                      {job.updated_at ? new Date(job.updated_at).toLocaleDateString() : 'Unknown'}
+                    </dd>
+                  </div>
+                  <div>
+                    <dt className="text-sm font-medium text-gray-500">Job ID</dt>
+                    <dd className="text-sm text-gray-900 font-mono">{job.job_id}</dd>
+                  </div>
+                </dl>
+              </div>
+            </div>
+          )}
+        </div>
       </div>
     </div>
   );
 }