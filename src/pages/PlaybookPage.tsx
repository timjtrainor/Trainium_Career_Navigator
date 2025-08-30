@@ .. @@
+import { BookOpen, Target, Users, TrendingUp } from 'lucide-react';
+
 export default function PlaybookPage() {
   return (
-    <main id="main">
-      <h1>Career Playbook</h1>
-    </main>
+    <div className="space-y-6">
+      <div className="card">
+        <div className="flex items-center space-x-3 mb-4">
+          <div className="p-2 bg-primary-100 rounded-lg">
+            <BookOpen className="w-6 h-6 text-primary-600" />
+          </div>
+          <div>
+            <h1 className="text-2xl font-semibold text-gray-900">Career Playbook</h1>
+            <p className="text-gray-600">Your personalized career development guide</p>
+          </div>
+        </div>
+      </div>

+      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
+        <div className="card hover:shadow-md transition-shadow cursor-pointer">
+          <div className="flex items-center space-x-3 mb-3">
+            <Target className="w-5 h-5 text-primary-600" />
+            <h3 className="font-medium text-gray-900">Goal Setting</h3>
+          </div>
+          <p className="text-sm text-gray-600">Define your career objectives and create actionable milestones.</p>
+        </div>
+        
+        <div className="card hover:shadow-md transition-shadow cursor-pointer">
+          <div className="flex items-center space-x-3 mb-3">
+            <Users className="w-5 h-5 text-primary-600" />
+            <h3 className="font-medium text-gray-900">Networking</h3>
+          </div>
+          <p className="text-sm text-gray-600">Build meaningful professional relationships and expand your network.</p>
+        </div>
+        
+        <div className="card hover:shadow-md transition-shadow cursor-pointer">
+          <div className="flex items-center space-x-3 mb-3">
+            <TrendingUp className="w-5 h-5 text-primary-600" />
+            <h3 className="font-medium text-gray-900">Skill Development</h3>
+          </div>
+          <p className="text-sm text-gray-600">Identify skill gaps and create learning plans for career advancement.</p>
+        </div>
+      </div>
+    </div>
   );
 }