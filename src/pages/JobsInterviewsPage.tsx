@@ .. @@
+import { Calendar, Clock, Video, MapPin } from 'lucide-react';
+import EmptyState from '../components/EmptyState';
+
 export default function JobsInterviewsPage() {
-  return <h1>Job Interviews (Coming Soon)</h1>;
+  // Mock data for demonstration
+  const interviews = [
+    {
+      id: '1',
+      title: 'Senior Software Engineer',
+      company: 'Acme Corporation',
+      date: '2024-01-20',
+      time: '2:00 PM',
+      type: 'video',
+      stage: 'Technical Interview',
+    },
+    {
+      id: '2',
+      title: 'Product Manager',
+      company: 'Beta Inc',
+      date: '2024-01-22',
+      time: '10:00 AM',
+      type: 'onsite',
+      stage: 'Final Round',
+    },
+  ];

+  return (
+    <div className="space-y-6">
+      {/* Header */}
+      <div className="card">
+        <div className="flex items-center space-x-3 mb-4">
+          <div className="p-2 bg-primary-100 rounded-lg">
+            <Calendar className="w-6 h-6 text-primary-600" />
+          </div>
+          <div>
+            <h1 className="text-2xl font-semibold text-gray-900">Interviews</h1>
+            <p className="text-gray-600">Manage your upcoming and past interviews</p>
+          </div>
+        </div>
+      </div>

+      {/* Quick Stats */}
+      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-primary-600">{interviews.length}</div>
+            <div className="text-sm text-gray-500">Scheduled Interviews</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-success-600">
+              {interviews.filter(i => i.type === 'video').length}
+            </div>
+            <div className="text-sm text-gray-500">Video Calls</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-warning-600">
+              {interviews.filter(i => i.type === 'onsite').length}
+            </div>
+            <div className="text-sm text-gray-500">On-site Visits</div>
+          </div>
+        </div>
+      </div>

+      {/* Interviews List */}
+      {interviews.length === 0 ? (
+        <EmptyState
+          icon={<Calendar className="w-12 h-12" />}
+          title="No interviews scheduled"
+          description="Your upcoming interviews will appear here once you start applying to jobs."
+        />
+      ) : (
+        <div className="space-y-4">
+          {interviews.map((interview) => (
+            <div key={interview.id} className="card hover:shadow-md transition-shadow">
+              <div className="flex items-center justify-between">
+                <div className="flex-1">
+                  <div className="flex items-center space-x-3 mb-2">
+                    <h3 className="font-semibold text-gray-900">{interview.title}</h3>
+                    <span className="pill-neutral">{interview.stage}</span>
+                  </div>
+                  <p className="text-gray-600 mb-3">{interview.company}</p>
+                  <div className="flex items-center space-x-6 text-sm text-gray-500">
+                    <div className="flex items-center space-x-1">
+                      <Calendar className="w-4 h-4" />
+                      <span>{new Date(interview.date).toLocaleDateString()}</span>
+                    </div>
+                    <div className="flex items-center space-x-1">
+                      <Clock className="w-4 h-4" />
+                      <span>{interview.time}</span>
+                    </div>
+                    <div className="flex items-center space-x-1">
+                      {interview.type === 'video' ? (
+                        <Video className="w-4 h-4" />
+                      ) : (
+                        <MapPin className="w-4 h-4" />
+                      )}
+                      <span className="capitalize">{interview.type}</span>
+                    </div>
+                  </div>
+                </div>
+                <div className="flex items-center space-x-2">
+                  <button className="btn-secondary text-sm">
+                    Reschedule
+                  </button>
+                  <button className="btn-primary text-sm">
+                    Join Call
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