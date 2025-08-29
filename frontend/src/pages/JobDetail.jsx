import { useParams } from 'react-router-dom';

export default function JobDetail() {
  const { id } = useParams();
  return <div>Job Detail for {id}</div>;
}
