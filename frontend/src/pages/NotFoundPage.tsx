import { Link } from 'react-router-dom';

interface Props {
  to: string;
}

export default function NotFoundPage({ to }: Props) {
  return (
    <main id="main">
      <h1>Page Not Found</h1>
      <p><Link to={to}>Go back</Link></p>
    </main>
  );
}
