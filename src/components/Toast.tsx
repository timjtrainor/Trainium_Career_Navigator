@@ .. @@
-import { useEffect } from 'react';
-import styles from './Toast.module.css';
+import { useEffect } from 'react';
+import { CheckCircle, AlertCircle, X } from 'lucide-react';
 
 interface Props {
   message: string;
+  type?: 'success' | 'error' | 'info';
   onDismiss: () => void;
 }
 
-export default function Toast({ message, onDismiss }: Props) {
+export default function Toast({ message, type = 'info', onDismiss }: Props) {
   useEffect(() => {
@@ .. @@
     return () => clearTimeout(timer);
   }, [onDismiss]);
 
+  const icons = {
+    success: CheckCircle,
+    error: AlertCircle,
+    info: AlertCircle,
+  };
+
+  const styles = {
+    success: 'bg-success-50 border-success-200 text-success-800',
+    error: 'bg-error-50 border-error-200 text-error-800',
+    info: 'bg-primary-50 border-primary-200 text-primary-800',
+  };
+
+  const Icon = icons[type];
+
   return (
-    <div className={styles.toast} role="status" aria-live="polite">
-      {message}
+    <div 
+      className={`
+        fixed bottom-4 right-4 z-50 max-w-sm w-full border rounded-lg p-4 shadow-lg animate-slide-in
+        ${styles[type]}
+      `}
+      role="status" 
+      aria-live="polite"
+    >
+      <div className="flex items-start space-x-3">
+        <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
+        <p className="text-sm font-medium flex-1">{message}</p>
+        <button
+          onClick={onDismiss}
+          className="flex-shrink-0 p-1 rounded-md hover:bg-black hover:bg-opacity-10 transition-colors"
+          aria-label="Dismiss"
+        >
+          <X className="w-4 h-4" />
+        </button>
+      </div>
     </div>
   );
 }