@@ .. @@
+import { Building, TrendingUp, Users, Star } from 'lucide-react';
+import EmptyState from '../components/EmptyState';
+
 export default function JobsCompaniesPage() {
-  return <h1>Companies</h1>;
+  // Mock data for demonstration
+  const companies = [
+    {
+      id: '1',
+      name: 'Acme Corporation',
+      jobCount: 5,
+      recommendedCount: 3,
+      industry: 'Technology',
+      size: 'Large (1000+ employees)',
+      rating: 4.2,
+    },
+    {
+      id: '2',
+      name: 'Beta Inc',
+      jobCount: 2,
+      recommendedCount: 1,
+      industry: 'Fintech',
+      size: 'Medium (100-1000 employees)',
+      rating: 3.8,
+    },
+  ];

+  return (
+    <div className="space-y-6">
+      {/* Header */}
+      <div className="card">
+        <div className="flex items-center space-x-3 mb-4">
+          <div className="p-2 bg-primary-100 rounded-lg">
+            <Building className="w-6 h-6 text-primary-600" />
+          </div>
+          <div>
+            <h1 className="text-2xl font-semibold text-gray-900">Companies</h1>
+            <p className="text-gray-600">Explore companies and their job opportunities</p>
+          </div>
+        </div>
+      </div>

+      {/* Quick Stats */}
+      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-gray-900">{companies.length}</div>
+            <div className="text-sm text-gray-500">Companies Tracked</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-primary-600">
+              {companies.reduce((sum, c) => sum + c.jobCount, 0)}
+            </div>
+            <div className="text-sm text-gray-500">Total Job Openings</div>
+          </div>
+        </div>
+        <div className="card">
+          <div className="text-center">
+            <div className="text-2xl font-bold text-success-600">
+              {companies.reduce((sum, c) => sum + c.recommendedCount, 0)}
+            </div>
+            <div className="text-sm text-gray-500">Recommended Positions</div>
+          </div>
+        </div>
+      </div>

+      {/* Companies List */}
+      {companies.length === 0 ? (
+        <EmptyState
+          icon={<Building className="w-12 h-12" />}
+          title="No companies tracked"
+          description="Companies will appear here as you discover and evaluate job opportunities."
+        />
+      ) : (
+        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
+          {companies.map((company) => (
+            <div key={company.id} className="card hover:shadow-md transition-shadow cursor-pointer">
+              <div className="flex items-start justify-between mb-4">
+                <div className="flex-1">
+                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
+                    {company.name}
+                  </h3>
+                  <p className="text-gray-600 text-sm mb-2">{company.industry}</p>
+                  <p className="text-gray-500 text-xs">{company.size}</p>
+                </div>
+                <div className="flex items-center space-x-1">
+                  <Star className="w-4 h-4 text-yellow-400 fill-current" />
+                  <span className="text-sm font-medium text-gray-700">{company.rating}</span>
+                </div>
+              </div>
+              
+              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
+                <div className="text-center">
+                  <div className="text-lg font-bold text-gray-900">{company.jobCount}</div>
+                  <div className="text-xs text-gray-500">Open Positions</div>
+                </div>
+                <div className="text-center">
+                  <div className="text-lg font-bold text-success-600">{company.recommendedCount}</div>
+                  <div className="text-xs text-gray-500">Recommended</div>
+                </div>
+              </div>
+            </div>
+          ))}
+        </div>
+      )}
+    </div>
+  );
 }