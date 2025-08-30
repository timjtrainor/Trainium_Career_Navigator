@@ .. @@
+import { useState } from 'react';
+import { FileText, Calendar, CheckCircle, Clock, XCircle } from 'lucide-react';
+import EmptyState from '../components/EmptyState';
+import DecisionPill from '../components/DecisionPill';
+
 export default function JobsApplicationsPage() {
-  return <h1>Job Applications</h1>;
+  const [filter, setFilter] = useState<'all' | 'pending' | 'accepted' | 'rejected'>('all');
+
+  // Mock data for demonstration
+  const applications = [
+    {
+      id: '1',
+      title: 'Senior Software Engineer',
+      company: 'Acme Corporation',
+      appliedDate: '2024-01-15',
+      status: 'pending',
+      stage: 'Application Review',
+    },
+    {
+      id: '2',
+      title: 'Product Manager',
+      company: 'Beta Inc',
+      appliedDate: '2024-01-12',
+      status: 'interview',
+      stage: 'Technical Interview',
+    },
+  ];

+  const stats = {
+    total: applications.length,
+    pending: applications.filter(a => a.status === 'pending').length,
+    interview: applications.filter(a => a.status === 'interview').length,
+    rejected: applications.filter(a => a.status === 'rejected').length,
+  };

+  return (
+    <div className="space-y-6">
+      {/* Stats Overview */}
+      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-primary-100 rounded-lg">
+              <FileText className="w-6 h-6 text-primary-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
+              <div className="text-sm text-gray-500">Total Applications</div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-warning-100 rounded-lg">
+              <Clock className="w-6 h-6 text-warning-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.pending}</div>
+              <div className="text-sm text-gray-500">Pending Review</div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="flex items-center space-x-3">
+            <div className="p-2 bg-success-100 rounded-lg">
+              <Calendar className="w-6 h-6 text-success-600" />
+            </div>
+            <div>
+              <div className="text-2xl font-bold text-gray-900">{stats.interview}</div>
+              <div className="text-sm text-gray-500">Interviews</div>
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
+              <div className="text-sm text-gray-500">Not Selected</div>
+            </div>
+          </div>
+        </div>
+      </div>

+      {/* Filter Tabs */}
+      <div className="card">
+        <div className="flex space-x-1 p-1 bg-gray-100 rounded-lg">
+          {[
+            { key: 'all', label: 'All Applications' },
+            { key: 'pending', label: 'Pending' },
+            { key: 'interview', label: 'Interviews' },
+            { key: 'rejected', label: 'Rejected' },
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
+              {tab.label}
+            </button>
+          ))}
+        </div>
+      </div>

+      {/* Applications List */}
+      {applications.length === 0 ? (
+        <EmptyState
+          icon={<FileText className="w-12 h-12" />}
+          title="No applications yet"
+          description="Applications you submit will be tracked here automatically."
+        />
+      ) : (
+        <div className="space-y-4">
+          {applications.map((app) => (
+            <div key={app.id} className="card hover:shadow-md transition-shadow">
+              <div className="flex items-center justify-between">
+                <div className="flex-1">
+                  <h3 className="font-semibold text-gray-900 mb-1">{app.title}</h3>
+                  <p className="text-gray-600 mb-2">{app.company}</p>
+                  <div className="flex items-center space-x-4 text-sm text-gray-500">
+                    <span>Applied {new Date(app.appliedDate).toLocaleDateString()}</span>
+                    <span>•</span>
+                    <span>{app.stage}</span>
+                  </div>
+                </div>
+                <div className="flex items-center space-x-3">
+                  <DecisionPill decision={app.status} />
+                  <button className="btn-ghost text-sm">
+                    Update Status
+                  </button>
+                </div>
+              </div>
+            </div>
+          ))}
+        </div>
+      )}
+    </div>
+  );
 }