@@ .. @@
+import { useQuery } from '@tanstack/react-query';
+import { TrendingUp, Clock, Target, AlertTriangle } from 'lucide-react';
+import LoadingSpinner from '../components/LoadingSpinner';
+
+interface OperationalMetrics {
+  error_rate: number;
+  avg_latency_ms: number;
+}
+
+interface UserMetrics {
+  fit_accuracy: number;
+  false_positives: number;
+  missed_opportunities: number;
+}
+
+interface BusinessMetrics {
+  application_rate: number;
+  application_volume: number;
+  conversion_ratio: number;
+}
+
 export default function ProgressPage() {
+  const { data: operational } = useQuery<OperationalMetrics>({
+    queryKey: ['metrics', 'operational'],
+    queryFn: async () => {
+      const resp = await fetch('/api/metrics/operational');
+      if (!resp.ok) throw new Error('Failed to fetch operational metrics');
+      return resp.json();
+    },
+    staleTime: 60000,
+  });
+
+  const { data: user } = useQuery<UserMetrics>({
+    queryKey: ['metrics', 'user'],
+    queryFn: async () => {
+      const resp = await fetch('/api/metrics/user');
+      if (!resp.ok) throw new Error('Failed to fetch user metrics');
+      return resp.json();
+    },
+    staleTime: 60000,
+  });
+
+  const { data: business } = useQuery<BusinessMetrics>({
+    queryKey: ['metrics', 'business'],
+    queryFn: async () => {
+      const resp = await fetch('/api/metrics/business');
+      if (!resp.ok) throw new Error('Failed to fetch business metrics');
+      return resp.json();
+    },
+    staleTime: 60000,
+  });
+
   return (
-    <main id="main">
-      <h1>Progress</h1>
-    </main>
+    <div className="space-y-6">
+      {/* System Health */}
+      <div>
+        <h2 className="text-lg font-semibold text-gray-900 mb-4">System Health</h2>
+        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
+          <div className="card">
+            <div className="flex items-center space-x-3">
+              <div className="p-2 bg-primary-100 rounded-lg">
+                <Clock className="w-6 h-6 text-primary-600" />
+              </div>
+              <div>
+                <div className="text-2xl font-bold text-gray-900">
+                  {operational ? Math.round(operational.avg_latency_ms) : '—'}ms
+                </div>
+                <div className="text-sm text-gray-500">Average Response Time</div>
+              </div>
+            </div>
+          </div>
+          
+          <div className="card">
+            <div className="flex items-center space-x-3">
+              <div className="p-2 bg-error-100 rounded-lg">
+                <AlertTriangle className="w-6 h-6 text-error-600" />
+              </div>
+              <div>
+                <div className="text-2xl font-bold text-gray-900">
+                  {operational ? (operational.error_rate * 100).toFixed(1) : '—'}%
+                </div>
+                <div className="text-sm text-gray-500">Error Rate (7 days)</div>
+              </div>
+            </div>
+          </div>
+        </div>
+      </div>

+      {/* User Experience */}
+      <div>
+        <h2 className="text-lg font-semibold text-gray-900 mb-4">User Experience</h2>
+        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
+          <div className="card">
+            <div className="flex items-center space-x-3">
+              <div className="p-2 bg-success-100 rounded-lg">
+                <Target className="w-6 h-6 text-success-600" />
+              </div>
+              <div>
+                <div className="text-2xl font-bold text-gray-900">
+                  {user ? (user.fit_accuracy * 100).toFixed(1) : '—'}%
+                </div>
+                <div className="text-sm text-gray-500">Fit Accuracy</div>
+              </div>
+            </div>
+          </div>
+          
+          <div className="card">
+            <div className="text-center">
+              <div className="text-2xl font-bold text-gray-900">
+                {user?.false_positives || 0}
+              </div>
+              <div className="text-sm text-gray-500">False Positives</div>
+            </div>
+          </div>
+          
+          <div className="card">
+            <div className="text-center">
+              <div className="text-2xl font-bold text-gray-900">
+                {user?.missed_opportunities || 0}
+              </div>
+              <div className="text-sm text-gray-500">Missed Opportunities</div>
+            </div>
+          </div>
+        </div>
+      </div>

+      {/* Business Metrics */}
+      <div>
+        <h2 className="text-lg font-semibold text-gray-900 mb-4">Application Metrics</h2>
+        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
+          <div className="card">
+            <div className="flex items-center space-x-3">
+              <div className="p-2 bg-primary-100 rounded-lg">
+                <TrendingUp className="w-6 h-6 text-primary-600" />
+              </div>
+              <div>
+                <div className="text-2xl font-bold text-gray-900">
+                  {business ? (business.application_rate * 100).toFixed(1) : '—'}%
+                </div>
+                <div className="text-sm text-gray-500">Application Rate</div>
+              </div>
+            </div>
+          </div>
+          
+          <div className="card">
+            <div className="text-center">
+              <div className="text-2xl font-bold text-gray-900">
+                {business?.application_volume || 0}
+              </div>
+              <div className="text-sm text-gray-500">Total Applications</div>
+            </div>
+          </div>
+        </div>
+      </div>
+    </div>
   );
 }