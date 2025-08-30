import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import NavBar from './components/NavBar';
import PlaybookPage from './pages/PlaybookPage';
import JobsLayout from './layouts/JobsLayout';
import JobsDiscoverPage from './pages/JobsDiscoverPage';
import JobsEvaluatePage from './pages/JobsEvaluatePage';
import JobsShortlistPage from './pages/JobsShortlistPage';
import JobsApplicationsPage from './pages/JobsApplicationsPage';
import JobsInterviewsPage from './pages/JobsInterviewsPage';
import JobsCompaniesPage from './pages/JobsCompaniesPage';
import JobDetailPage from './pages/JobDetailPage';
import EngagementPage from './pages/EngagementPage';
import ContactsPage from './pages/ContactsPage';
import ProgressPage from './pages/ProgressPage';
import NotFoundPage from './pages/NotFoundPage';
import JobDrawer from './components/JobDrawer';

export default function App() {
  const location = useLocation();
  const state = location.state as { backgroundLocation?: Location } | undefined;

  return (
    <div>
      <NavBar />
      <Routes location={state?.backgroundLocation || location}>
        <Route path="/playbook" element={<PlaybookPage />} />
        <Route path="/jobs" element={<JobsLayout />}>
          <Route index element={<Navigate to="discover" replace />} />
          <Route path="discover" element={<JobsDiscoverPage />} />
          <Route path="evaluate" element={<JobsEvaluatePage />} />
          <Route path="shortlist" element={<JobsShortlistPage />} />
          <Route path="applications" element={<JobsApplicationsPage />} />
          <Route path="interviews" element={<JobsInterviewsPage />} />
          <Route path="companies" element={<JobsCompaniesPage />} />
          <Route path=":id" element={<JobDetailPage />} />
        </Route>
        <Route path="/engagement" element={<EngagementPage />} />
        <Route path="/contacts" element={<ContactsPage />} />
        <Route path="/progress" element={<ProgressPage />} />
        <Route path="*" element={<NotFoundPage to="/jobs/discover" />} />
      </Routes>
      {state?.backgroundLocation && (
        <Routes>
          <Route path="/jobs/:id" element={<JobDrawer />} />
        </Routes>
      )}
    </div>
  );
}
