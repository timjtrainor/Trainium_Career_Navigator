@@ .. @@
-import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
-import NavBar from './components/NavBar';
+import { useState } from 'react';
+import { Routes, Route, Navigate, useLocation, useSearchParams } from 'react-router-dom';
+import Sidebar from './components/Sidebar';
+import Header from './components/Header';
 import PlaybookPage from './pages/PlaybookPage';
-import JobsLayout from './layouts/JobsLayout';
+import JobsSubNav from './components/JobsSubNav';
 import JobsDiscoverPage from './pages/JobsDiscoverPage';
@@ .. @@
 import JobDetailPage from './pages/JobDetailPage';
+import AddJobModal from './components/AddJobModal';
 import EngagementPage from './pages/EngagementPage';
@@ .. @@
 import JobDrawer from './components/JobDrawer';
 
 export default function App() {
+  const [sidebarOpen, setSidebarOpen] = useState(false);
+  const [showAddJobModal, setShowAddJobModal] = useState(false);
+  const [searchParams, setSearchParams] = useSearchParams();
+  const search = searchParams.get('query') || '';
   const location = useLocation();
   const state = location.state as { backgroundLocation?: Location } | undefined;
+  const isJobsPage = location.pathname.startsWith('/jobs');
+
+  const handleSearchChange = (value: string) => {
+    const params = new URLSearchParams(searchParams);
+    if (value) {
+      params.set('query', value);
+    } else {
+      params.delete('query');
+    }
+    params.delete('page'); // Reset to first page on search
+    setSearchParams(params, { replace: true });
+  };
 
   return (
-    <div>
-      <NavBar />
-      <Routes location={state?.backgroundLocation || location}>
-        <Route path="/playbook" element={<PlaybookPage />} />
-        <Route path="/jobs" element={<JobsLayout />}>
-          <Route index element={<Navigate to="discover" replace />} />
-          <Route path="discover" element={<JobsDiscoverPage />} />
-          <Route path="evaluate" element={<JobsEvaluatePage />} />
-          <Route path="shortlist" element={<JobsShortlistPage />} />
-          <Route path="applications" element={<JobsApplicationsPage />} />
-          <Route path="interviews" element={<JobsInterviewsPage />} />
-          <Route path="companies" element={<JobsCompaniesPage />} />
-          <Route path=":id" element={<JobDetailPage />} />
-        </Route>
-        <Route path="/engagement" element={<EngagementPage />} />
-        <Route path="/contacts" element={<ContactsPage />} />
-        <Route path="/progress" element={<ProgressPage />} />
-        <Route path="*" element={<NotFoundPage to="/jobs/discover" />} />
-      </Routes>
+    <div className="min-h-screen bg-gray-50">
+      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
+      
+      <div className="lg:ml-64">
+        <Header 
+          onSidebarToggle={() => setSidebarOpen(true)}
+          onAddJob={() => setShowAddJobModal(true)}
+          search={search}
+          onSearchChange={handleSearchChange}
+        />
+        
+        {isJobsPage && <JobsSubNav />}
+        
+        <main className="p-6">
+          <Routes location={state?.backgroundLocation || location}>
+            <Route path="/playbook" element={<PlaybookPage />} />
+            <Route path="/jobs" element={<Navigate to="/jobs/discover" replace />} />
+            <Route path="/jobs/discover" element={<JobsDiscoverPage />} />
+            <Route path="/jobs/evaluate" element={<JobsEvaluatePage />} />
+            <Route path="/jobs/shortlist" element={<JobsShortlistPage />} />
+            <Route path="/jobs/applications" element={<JobsApplicationsPage />} />
+            <Route path="/jobs/interviews" element={<JobsInterviewsPage />} />
+            <Route path="/jobs/companies" element={<JobsCompaniesPage />} />
+            <Route path="/jobs/:id" element={<JobDetailPage />} />
+            <Route path="/engagement" element={<EngagementPage />} />
+            <Route path="/contacts" element={<ContactsPage />} />
+            <Route path="/progress" element={<ProgressPage />} />
+            <Route path="*" element={<NotFoundPage to="/jobs/discover" />} />
+          </Routes>
+        </main>
+      </div>
+      
+      {/* Modals */}
+      {showAddJobModal && (
+        <AddJobModal onClose={() => setShowAddJobModal(false)} />
+      )}
+      
       {state?.backgroundLocation && (
         <Routes>
           <Route path="/jobs/:id" element={<JobDrawer />} />