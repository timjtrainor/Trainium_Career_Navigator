import { Link, useLocation } from 'react-router-dom';

export default function JobsDiscoverPage() {
  const location = useLocation();
  return (
    <div>
      <h1>Discover Jobs</h1>
      <ul>
        <li><Link to="/jobs/1" state={{ backgroundLocation: location }}>Sample Job 1</Link></li>
      </ul>
    </div>
  );
}
