interface DecisionPillProps {
  decision: string;
  size?: 'sm' | 'md';
}

const decisionStyles: Record<string, string> = {
  'recommended': 'pill-success',
  'approved': 'pill-success',
  'rejected': 'pill-error',
  'bad_fit': 'pill-error',
  'pending': 'pill-warning',
  'evaluating': 'pill-warning',
  'undecided': 'pill-neutral',
};

export default function DecisionPill({ decision, size = 'sm' }: DecisionPillProps) {
  const baseClass = decisionStyles[decision] || 'pill-neutral';
  const sizeClass = size === 'md' ? 'px-3 py-1 text-sm' : 'px-2.5 py-0.5 text-xs';
  
  return (
    <span className={`pill ${baseClass} ${sizeClass}`}>
      {decision.replace('_', ' ')}
    </span>
  );
}