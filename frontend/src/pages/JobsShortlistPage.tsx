import { Link, useLocation } from 'react-router-dom';

export default function JobsShortlistPage() {
  const location = useLocation();
  return (
    <div>
      <h1>Shortlisted Jobs</h1>
      <ul>
        <li><Link to="/jobs/2" state={{ backgroundLocation: location }}>Sample Job 2</Link></li>
      </ul>
    </div>
  );
}
