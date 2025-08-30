import { Search, Plus, Menu } from 'lucide-react';
import { useLocation } from 'react-router-dom';

interface HeaderProps {
  onSidebarToggle: () => void;
  onAddJob: () => void;
  search: string;
  onSearchChange: (value: string) => void;
}

const pageTitles: Record<string, string> = {
  '/jobs/discover': 'Discover Jobs',
  '/jobs/evaluate': 'Evaluate Jobs',
  '/jobs/shortlist': 'Shortlist',
  '/jobs/applications': 'Applications',
  '/jobs/interviews': 'Interviews',
  '/jobs/companies': 'Companies',
  '/playbook': 'Career Playbook',
  '/engagement': 'Engagement',
  '/contacts': 'Contacts',
  '/progress': 'Progress',
};

export default function Header({ onSidebarToggle, onAddJob, search, onSearchChange }: HeaderProps) {
  const location = useLocation();
  const currentTitle = pageTitles[location.pathname] || 'Jobs';
  const isJobsPage = location.pathname.startsWith('/jobs');
  const showSearch = location.pathname.match(/\/jobs\/(discover|shortlist)/);

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onSidebarToggle}
            className="lg:hidden p-2 rounded-md hover:bg-gray-100"
            aria-label="Open sidebar"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-2xl font-semibold text-gray-900">{currentTitle}</h1>
        </div>

        <div className="flex items-center space-x-4">
          {showSearch && (
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="search"
                placeholder="Search jobs..."
                className="input pl-10 w-80"
                value={search}
                onChange={(e) => onSearchChange(e.target.value)}
              />
            </div>
          )}
          
          {isJobsPage && (
            <button
              onClick={onAddJob}
              className="btn-primary flex items-center space-x-2"
            >
              <Plus className="w-4 h-4" />
              <span>Add Job</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}