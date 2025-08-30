import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  BookOpen, 
  Briefcase, 
  Users, 
  MessageSquare, 
  TrendingUp,
  Menu,
  X,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

const navItems = [
  { 
    to: '/playbook', 
    label: 'Career Playbook', 
    icon: BookOpen,
    children: []
  },
  { 
    to: '/jobs', 
    label: 'Jobs', 
    icon: Briefcase,
    children: [
      { to: '/jobs/discover', label: 'Discover' },
      { to: '/jobs/evaluate', label: 'Evaluate' },
      { to: '/jobs/shortlist', label: 'Shortlist' },
      { to: '/jobs/applications', label: 'Applications' },
      { to: '/jobs/interviews', label: 'Interviews' },
      { to: '/jobs/companies', label: 'Companies' },
    ]
  },
  { 
    to: '/engagement', 
    label: 'Engagement', 
    icon: MessageSquare,
    children: []
  },
  { 
    to: '/contacts', 
    label: 'Contacts', 
    icon: Users,
    children: []
  },
  { 
    to: '/progress', 
    label: 'Progress', 
    icon: TrendingUp,
    children: []
  },
];

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const location = useLocation();
  const [expandedItems, setExpandedItems] = useState<string[]>(['/jobs']);

  const isActive = (path: string) => {
    if (path === '/jobs') {
      return location.pathname.startsWith('/jobs');
    }
    return location.pathname === path;
  };

  const isChildActive = (parentPath: string, childPath: string) => {
    return location.pathname === childPath;
  };

  const toggleExpanded = (path: string) => {
    setExpandedItems(prev => 
      prev.includes(path) 
        ? prev.filter(p => p !== path)
        : [...prev, path]
    );
  };

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 z-50 h-full w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:z-auto
      `}>
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <Link to="/jobs/discover" className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">T</span>
            </div>
            <span className="text-xl font-semibold text-gray-900">Trainium</span>
          </Link>
          <button
            onClick={onToggle}
            className="lg:hidden p-1 rounded-md hover:bg-gray-100"
            aria-label="Close sidebar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.to);
            const expanded = expandedItems.includes(item.to);
            const hasChildren = item.children.length > 0;

            return (
              <div key={item.to}>
                <div className="flex items-center">
                  <Link
                    to={item.to}
                    className={`
                      flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors flex-1
                      ${active 
                        ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600' 
                        : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                    onClick={() => !hasChildren && onToggle()}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                  {hasChildren && (
                    <button
                      onClick={() => toggleExpanded(item.to)}
                      className="p-1 rounded hover:bg-gray-100"
                      aria-label={`${expanded ? 'Collapse' : 'Expand'} ${item.label}`}
                    >
                      {expanded ? (
                        <ChevronDown className="w-4 h-4 text-gray-500" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-gray-500" />
                      )}
                    </button>
                  )}
                </div>
                
                {hasChildren && expanded && (
                  <div className="ml-8 mt-2 space-y-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.to}
                        to={child.to}
                        className={`
                          block px-3 py-2 rounded-lg text-sm transition-colors
                          ${isChildActive(item.to, child.to)
                            ? 'bg-primary-50 text-primary-700 font-medium'
                            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                          }
                        `}
                        onClick={onToggle}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </aside>
    </>
  );
}