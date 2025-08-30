import { Link, useLocation } from 'react-router-dom';

const tabs = [
  { to: '/jobs/discover', label: 'Discover' },
  { to: '/jobs/evaluate', label: 'Evaluate' },
  { to: '/jobs/shortlist', label: 'Shortlist' },
  { to: '/jobs/applications', label: 'Applications' },
  { to: '/jobs/interviews', label: 'Interviews' },
  { to: '/jobs/companies', label: 'Companies' },
];

export default function JobsSubNav() {
  const location = useLocation();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="px-6">
        <div className="flex space-x-8 overflow-x-auto scrollbar-hide">
          {tabs.map((tab) => {
            const isActive = location.pathname === tab.to;
            return (
              <Link
                key={tab.to}
                to={tab.to}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors
                  ${isActive
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                {tab.label}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}