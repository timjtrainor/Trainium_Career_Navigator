import { useParams } from 'react-router-dom';

export default function JobDetailPage() {
  const { id } = useParams();
  return (
    <main id="main">
      <h1>Job Detail {id}</h1>
    </main>
  );
}
