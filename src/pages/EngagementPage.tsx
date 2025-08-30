@@ .. @@
+import { MessageSquare, Users, Calendar, TrendingUp } from 'lucide-react';
+
 export default function EngagementPage() {
   return (
-    <main id="main">
-      <h1>Engagement</h1>
-    </main>
+    <div className="space-y-6">
+      <div className="card">
+        <div className="flex items-center space-x-3 mb-4">
+          <div className="p-2 bg-primary-100 rounded-lg">
+            <MessageSquare className="w-6 h-6 text-primary-600" />
+          </div>
+          <div>
+            <h1 className="text-2xl font-semibold text-gray-900">Engagement</h1>
+            <p className="text-gray-600">Track your networking and outreach activities</p>
+          </div>
+        </div>
+      </div>

+      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-gray-900">24</div>
+            <div className="text-sm text-gray-500">Connections Made</div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-primary-600">12</div>
+            <div className="text-sm text-gray-500">Messages Sent</div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-success-600">8</div>
+            <div className="text-sm text-gray-500">Responses Received</div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-warning-600">3</div>
+            <div className="text-sm text-gray-500">Meetings Scheduled</div>
+          </div>
+        </div>
+      </div>

+      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
+        <div className="card">
+          <h3 className="font-medium text-gray-900 mb-4">Recent Activity</h3>
+          <div className="space-y-3">
+            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
+              <Users className="w-4 h-4 text-primary-600" />
+              <div className="flex-1">
+                <p className="text-sm font-medium text-gray-900">Connected with Sarah Chen</p>
+                <p className="text-xs text-gray-500">2 hours ago</p>
+              </div>
+            </div>
+            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
+              <MessageSquare className="w-4 h-4 text-success-600" />
+              <div className="flex-1">
+                <p className="text-sm font-medium text-gray-900">Sent follow-up message</p>
+                <p className="text-xs text-gray-500">1 day ago</p>
+              </div>
+            </div>
+            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
+              <Calendar className="w-4 h-4 text-warning-600" />
+              <div className="flex-1">
+                <p className="text-sm font-medium text-gray-900">Coffee chat scheduled</p>
+                <p className="text-xs text-gray-500">3 days ago</p>
+              </div>
+            </div>
+          </div>
+        </div>
+        
+        <div className="card">
+          <h3 className="font-medium text-gray-900 mb-4">Engagement Goals</h3>
+          <div className="space-y-4">
+            <div>
+              <div className="flex justify-between text-sm mb-1">
+                <span className="text-gray-700">Weekly Connections</span>
+                <span className="text-gray-500">8/10</span>
+              </div>
+              <div className="w-full bg-gray-200 rounded-full h-2">
+                <div className="bg-primary-600 h-2 rounded-full" style={{ width: '80%' }}></div>
+              </div>
+            </div>
+            
+            <div>
+              <div className="flex justify-between text-sm mb-1">
+                <span className="text-gray-700">Follow-up Messages</span>
+                <span className="text-gray-500">5/8</span>
+              </div>
+              <div className="w-full bg-gray-200 rounded-full h-2">
+                <div className="bg-success-600 h-2 rounded-full" style={{ width: '62.5%' }}></div>
+              </div>
+            </div>
+            
+            <div>
+              <div className="flex justify-between text-sm mb-1">
+                <span className="text-gray-700">Coffee Chats</span>
+                <span className="text-gray-500">3/5</span>
+              </div>
+              <div className="w-full bg-gray-200 rounded-full h-2">
+                <div className="bg-warning-600 h-2 rounded-full" style={{ width: '60%' }}></div>
+              </div>
+            </div>
+          </div>
+        </div>
+      </div>
+    </div>
   );
 }