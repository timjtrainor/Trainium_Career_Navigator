@@ .. @@
-import { Link, useLocation } from 'react-router-dom';
+import { useQuery } from '@tanstack/react-query';
+import { Star, TrendingUp } from 'lucide-react';
+import JobCard from '../components/JobCard';
+import EmptyState from '../components/EmptyState';
+import LoadingSpinner from '../components/LoadingSpinner';
+
+interface Recommendation {
+  job_id: string;
+  title?: string;
+  company?: string;
+  url?: string;
+  rationale?: string;
+  confidence: number;
+}
 
 export default function JobsShortlistPage() {
-  const location = useLocation();
+  const { data: recommendations, isLoading, error } = useQuery<Recommendation[]>({
+    queryKey: ['recommendations'],
+    queryFn: async () => {
+      const resp = await fetch('/api/recommendations');
+      if (!resp.ok) throw new Error('Failed to fetch recommendations');
+      return resp.json();
+    },
+    staleTime: 30000,
+  });
+
   return (
-    <div>
-      <h1>Shortlisted Jobs</h1>
-      <ul>
-        <li><Link to="/jobs/2" state={{ backgroundLocation: location }}>Sample Job 2</Link></li>
-      </ul>
+    <div className="space-y-6">
+      {/* Header Stats */}
+      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-primary-100 rounded-lg">
+              <Star className="w-6 h-6 text-primary-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">
+                {recommendations?.length || 0}
+              </div>
+              <div className="text-sm text-gray-500">Recommended Jobs</div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-success-100 rounded-lg">
+              <TrendingUp className="w-6 h-6 text-success-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">
+                {recommendations ? Math.round(recommendations.reduce((acc, r) => acc + r.confidence, 0) / recommendations.length * 100) || 0 : 0}%
+              </div>
+              <div className="text-sm text-gray-500">Avg. Confidence</div>
+            </div>
+          </div>
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
+          <p className="text-error-700 text-center">Failed to load recommendations. Please try again.</p>
+        </div>
+      )}

+      {/* Empty State */}
+      {!isLoading && recommendations && recommendations.length === 0 && (
+        <EmptyState
+          icon={<Star className="w-12 h-12" />}
+          title="No recommendations yet"
+          description="Jobs will appear here once our AI personas have evaluated them positively."
+        />
+      )}

+      {/* Recommendations List */}
+      {recommendations && recommendations.length > 0 && (
+        <div className="space-y-6">
+          {recommendations.map((rec) => (
+            <div key={rec.job_id} className="card">
+              <div className="flex items-start justify-between mb-4">
+                <div className="flex-1">
+                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
+                    {rec.title || 'Untitled Position'}
+                  </h3>
+                  <p className="text-gray-600">{rec.company}</p>
+                </div>
+                <div className="flex items-center space-x-2">
+                  <span className="pill-success">
+                    {Math.round(rec.confidence * 100)}% match
+                  </span>
+                  {rec.url && (
+                    <a
+                      href={rec.url}
+                      target="_blank"
+                      rel="noopener noreferrer"
+                      className="btn-secondary text-sm"
+                    >
+                      Apply
+                    </a>
+                  )}
+                </div>
+              </div>
+              
+              {rec.rationale && (
+                <div className="bg-gray-50 rounded-lg p-4">
+                  <h4 className="font-medium text-gray-900 mb-2">Why this job fits:</h4>
+                  <p className="text-gray-700 text-sm">{rec.rationale}</p>
+                </div>
+              )}
+            </div>
+          ))}
+        </div>
+      )}
     </div>
   );
 }