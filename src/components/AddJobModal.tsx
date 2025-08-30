@@ .. @@
-import { useEffect, useRef, useState } from 'react';
+import { useEffect, useRef, useState } from 'react';
 import { useQueryClient } from '@tanstack/react-query';
-import styles from './AddJobModal.module.css';
+import { X } from 'lucide-react';
+import LoadingSpinner from './LoadingSpinner';
 
 interface Props {
@@ .. @@
   const [error, setError] = useState<string | null>(null);
+  const [isSubmitting, setIsSubmitting] = useState(false);
 
   useEffect(() => {
@@ .. @@
   const handleSubmit = async (e: React.FormEvent) => {
     e.preventDefault();
+    setIsSubmitting(true);
     setError(null);
-    const resp = await fetch('/api/jobs', {
-      method: 'POST',
-      headers: { 'Content-Type': 'application/json' },
-      body: JSON.stringify({
-        title: form.title,
-        company: form.company,
-        url: form.url,
-        location: form.location || undefined,
-        description: form.description || undefined,
-      }),
-    });
-    if (!resp.ok) {
-      setError('Failed to save job');
-      return;
+    
+    try {
+      const resp = await fetch('/api/jobs', {
+        method: 'POST',
+        headers: { 'Content-Type': 'application/json' },
+        body: JSON.stringify({
+          title: form.title,
+          company: form.company,
+          url: form.url,
+          location: form.location || undefined,
+          description: form.description || undefined,
+        }),
+      });
+      
+      if (!resp.ok) {
+        const errorData = await resp.json().catch(() => ({}));
+        setError(errorData.detail || 'Failed to save job');
+        return;
+      }
+      
+      queryClient.invalidateQueries({ queryKey: ['jobs'] });
+      onClose();
+    } catch (err) {
+      setError('Network error occurred');
+    } finally {
+      setIsSubmitting(false);
     }
-    queryClient.invalidateQueries({ queryKey: ['jobs'] });
-    onClose();
   };
 
   return (
-    <div className={styles.backdrop} role="dialog" aria-modal="true" onClick={onClose}>
-      <div className={styles.modal} ref={ref} onClick={(e) => e.stopPropagation()}>
-        <h2 id="add-job-title">Add Job</h2>
-        <form onSubmit={handleSubmit}>
-          <label>
-            Job Title
-            <input
-              name="title"
-              value={form.title}
-              onChange={handleChange}
-              required
-            />
-          </label>
-          <label>
-            Company
-            <input
-              name="company"
-              value={form.company}
-              onChange={handleChange}
-              required
-            />
-          </label>
-          <label>
-            URL
-            <input
-              name="url"
-              type="url"
-              value={form.url}
-              onChange={handleChange}
-              required
-            />
-          </label>
-          <label>
-            Location
-            <input name="location" value={form.location} onChange={handleChange} />
-          </label>
-          <label>
-            Description
-            <textarea
-              name="description"
-              value={form.description}
-              onChange={handleChange}
-            />
-          </label>
-          {error && <p role="alert">{error}</p>}
-          <div>
-            <button type="submit">Save</button>
-            <button type="button" onClick={onClose}>
-              Cancel
-            </button>
+    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 animate-fade-in" role="dialog" aria-modal="true" onClick={onClose}>
+      <div 
+        ref={ref} 
+        className="bg-white rounded-xl shadow-xl w-full max-w-md animate-fade-in"
+        onClick={(e) => e.stopPropagation()}
+      >
+        {/* Header */}
+        <div className="flex items-center justify-between p-6 border-b border-gray-200">
+          <h2 className="text-lg font-semibold text-gray-900">Add New Job</h2>
+          <button
+            onClick={onClose}
+            className="p-2 rounded-md hover:bg-gray-100 transition-colors"
+            aria-label="Close modal"
+          >
+            <X className="w-5 h-5" />
+          </button>
+        </div>
+
+        {/* Form */}
+        <form onSubmit={handleSubmit} className="p-6 space-y-4">
+          <div>
+            <label className="block text-sm font-medium text-gray-700 mb-1">
+              Job Title *
+            </label>
+            <input
+              name="title"
+              value={form.title}
+              onChange={handleChange}
+              required
+              className="input"
+              placeholder="e.g. Senior Software Engineer"
+            />
+          </div>
+
+          <div>
+            <label className="block text-sm font-medium text-gray-700 mb-1">
+              Company *
+            </label>
+            <input
+              name="company"
+              value={form.company}
+              onChange={handleChange}
+              required
+              className="input"
+              placeholder="e.g. Acme Corporation"
+            />
+          </div>
+
+          <div>
+            <label className="block text-sm font-medium text-gray-700 mb-1">
+              Job URL *
+            </label>
+            <input
+              name="url"
+              type="url"
+              value={form.url}
+              onChange={handleChange}
+              required
+              className="input"
+              placeholder="https://..."
+            />
+          </div>
+
+          <div>
+            <label className="block text-sm font-medium text-gray-700 mb-1">
+              Location
+            </label>
+            <input
+              name="location"
+              value={form.location}
+              onChange={handleChange}
+              className="input"
+              placeholder="e.g. San Francisco, CA or Remote"
+            />
+          </div>
+
+          <div>
+            <label className="block text-sm font-medium text-gray-700 mb-1">
+              Description
+            </label>
+            <textarea
+              name="description"
+              value={form.description}
+              onChange={handleChange}
+              rows={4}
+              className="input resize-none"
+              placeholder="Brief job description..."
+            />
+          </div>
+
+          {error && (
+            <div className="p-3 bg-error-50 border border-error-200 rounded-lg">
+              <p className="text-sm text-error-700" role="alert">{error}</p>
+            </div>
+          )}
+
+          <div className="flex items-center justify-end space-x-3 pt-4">
+            <button
+              type="button"
+              onClick={onClose}
+              className="btn-secondary"
+              disabled={isSubmitting}
+            >
+              Cancel
+            </button>
+            <button
+              type="submit"
+              className="btn-primary flex items-center space-x-2"
+              disabled={isSubmitting}
+            >
+              {isSubmitting && <LoadingSpinner size="sm" />}
+              <span>{isSubmitting ? 'Saving...' : 'Save Job'}</span>
+            </button>
           </div>
         </form>
       </div>