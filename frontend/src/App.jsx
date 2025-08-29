import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Discover from './pages/Discover';
import Progress from './pages/Progress';
import JobDetail from './pages/JobDetail';
import Placeholder from './pages/Placeholder';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}> 
        <Route path="jobs/discover" element={<Discover />} />
        <Route path="jobs/evaluate" element={<Placeholder title="Evaluate Jobs" />} />
        <Route path="jobs/shortlist" element={<Placeholder title="Shortlist" />} />
        <Route path="jobs/applications" element={<Placeholder title="Applications" />} />
        <Route path="jobs/interviews" element={<Placeholder title="Interviews" />} />
        <Route path="jobs/companies" element={<Placeholder title="Companies" />} />
        <Route path="jobs/:id" element={<JobDetail />} />
        <Route path="progress" element={<Progress />} />
        <Route path="playbook" element={<Placeholder title="Playbook" />} />
        <Route path="engagement" element={<Placeholder title="Engagement" />} />
        <Route path="contacts" element={<Placeholder title="Contacts" />} />
      </Route>
    </Routes>
  );
}
