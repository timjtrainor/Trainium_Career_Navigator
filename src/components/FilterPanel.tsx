import { Filter, X } from 'lucide-react';

interface FilterPanelProps {
  sources: string[];
  selectedSources: string[];
  onSourcesChange: (sources: string[]) => void;
  since: string;
  onSinceChange: (since: string) => void;
  hideRejected: boolean;
  onHideRejectedChange: (hide: boolean) => void;
  onReset: () => void;
}

export default function FilterPanel({
  sources,
  selectedSources,
  onSourcesChange,
  since,
  onSinceChange,
  hideRejected,
  onHideRejectedChange,
  onReset,
}: FilterPanelProps) {
  const hasActiveFilters = selectedSources.length > 0 || since || hideRejected;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <h3 className="font-medium text-gray-900">Filters</h3>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="text-sm text-gray-500 hover:text-gray-700 flex items-center space-x-1"
          >
            <X className="w-3 h-3" />
            <span>Reset</span>
          </button>
        )}
      </div>

      <div className="space-y-4">
        {/* Sources */}
        {sources.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Sources
            </label>
            <div className="space-y-2">
              {sources.map((source) => (
                <label key={source} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(source)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        onSourcesChange([...selectedSources, source]);
                      } else {
                        onSourcesChange(selectedSources.filter(s => s !== source));
                      }
                    }}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700 capitalize">{source}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Time Range */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time Range
          </label>
          <select
            value={since}
            onChange={(e) => onSinceChange(e.target.value)}
            className="select"
          >
            <option value="">Any time</option>
            <option value="24h">Last 24 hours</option>
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
          </select>
        </div>

        {/* Hide Options */}
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={hideRejected}
              onChange={(e) => onHideRejectedChange(e.target.checked)}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span className="ml-2 text-sm text-gray-700">
              Hide rejected & bad fit jobs
            </span>
          </label>
        </div>
      </div>
    </div>
  );
}