@@ .. @@
+import { Users, Plus, Search, Mail, Phone, Building } from 'lucide-react';
+import EmptyState from '../components/EmptyState';
+
 export default function ContactsPage() {
   return (
-    <main id="main">
-      <h1>Contacts</h1>
-    </main>
+    <div className="space-y-6">
+      <div className="flex items-center justify-between">
+        <div className="flex items-center space-x-3">
+          <div className="p-2 bg-primary-100 rounded-lg">
+            <Users className="w-6 h-6 text-primary-600" />
+          </div>
+          <div>
+            <h1 className="text-2xl font-semibold text-gray-900">Contacts</h1>
+            <p className="text-gray-600">Manage your professional network</p>
+          </div>
+        </div>
+        <button className="btn-primary flex items-center space-x-2">
+          <Plus className="w-4 h-4" />
+          <span>Add Contact</span>
+        </button>
+      </div>

+      {/* Search and Filters */}
+      <div className="card">
+        <div className="flex items-center space-x-4">
+          <div className="relative flex-1">
+            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
+            <input
+              type="search"
+              placeholder="Search contacts..."
+              className="input pl-10"
+            />
+          </div>
+          <select className="select w-48">
+            <option value="">All Companies</option>
+            <option value="acme">Acme Corp</option>
+            <option value="beta">Beta Inc</option>
+          </select>
+        </div>
+      </div>

+      {/* Contacts List */}
+      <EmptyState
+        icon={<Users className="w-12 h-12" />}
+        title="No contacts yet"
+        description="Start building your professional network by adding contacts from companies you're interested in."
+        action={
+          <button className="btn-primary flex items-center space-x-2">
+            <Plus className="w-4 h-4" />
+            <span>Add Your First Contact</span>
+          </button>
+        }
+      />
+    </div>
   );
 }