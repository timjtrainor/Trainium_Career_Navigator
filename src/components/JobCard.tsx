import { Link, useLocation } from 'react-router-dom';
import { ExternalLink, Clock, MapPin, Building } from 'lucide-react';
import DecisionPill from './DecisionPill';

interface Job {
  id: string;
  title?: string;
  company?: string;
  source?: string;
  updated_at?: string;
  decision?: string;
  location?: string;
  description?: string;
}

interface JobCardProps {
  job: Job;
  onAnalyze?: (id: string) => void;
  showAnalyzeButton?: boolean;
}

function formatRelative(value?: string) {
  if (!value) return '';
  const date = new Date(value);
  const diff = Date.now() - date.getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function JobCard({ job, onAnalyze, showAnalyzeButton = true }: JobCardProps) {
  const location = useLocation();

  return (
    <div className="card hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-2">
            <Link
              to={`/jobs/${job.id}`}
              state={{ backgroundLocation: location }}
              className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors"
            >
              {job.title || 'Untitled Position'}
            </Link>
            {job.decision && <DecisionPill decision={job.decision} />}
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
            {job.company && (
              <div className="flex items-center space-x-1">
                <Building className="w-4 h-4" />
                <span>{job.company}</span>
              </div>
            )}
            {job.location && (
              <div className="flex items-center space-x-1">
                <MapPin className="w-4 h-4" />
                <span>{job.location}</span>
              </div>
            )}
            {job.updated_at && (
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{formatRelative(job.updated_at)}</span>
              </div>
            )}
          </div>

          {job.description && (
            <p className="text-gray-600 text-sm line-clamp-2 mb-4">
              {job.description}
            </p>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-2">
          {job.source && (
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {job.source}
            </span>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          {showAnalyzeButton && onAnalyze && (
            <button
              onClick={() => onAnalyze(job.id)}
              className="btn-secondary text-xs"
            >
              Analyze
            </button>
          )}
          <Link
            to={`/jobs/${job.id}`}
            state={{ backgroundLocation: location }}
            className="btn-ghost text-xs flex items-center space-x-1"
          >
            <span>View</span>
            <ExternalLink className="w-3 h-3" />
          </Link>
        </div>
      </div>
    </div>
  );
}