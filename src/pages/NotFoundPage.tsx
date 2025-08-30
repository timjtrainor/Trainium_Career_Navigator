@@ .. @@
-import { Link } from 'react-router-dom';
+import { Link } from 'react-router-dom';
+import { Home } from 'lucide-react';
+import EmptyState from '../components/EmptyState';
 
 interface Props {
@@ .. @@
 
 export default function NotFoundPage({ to }: Props) {
   return (
-    <main id="main">
-      <h1>Page Not Found</h1>
-      <p><Link to={to}>Go back</Link></p>
-    </main>
+    <div className="py-12">
+      <EmptyState
+        icon={<Home className="w-12 h-12" />}
+        title="Page Not Found"
+        description="The page you're looking for doesn't exist or has been moved."
+        action={
+          <Link to={to} className="btn-primary">
+            Go to Jobs
+          </Link>
+        }
+      />
+    </div>
   );
 }