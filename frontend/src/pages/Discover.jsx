import JobCard from '../components/JobCard';
import styles from './Discover.module.css';

const sampleJobs = [
  {
    company: 'Amazon',
    title: 'Senior UI Designer',
    location: 'Remote',
    posted: 'Jan 25, 2025'
  },
  {
    company: 'Google',
    title: 'Product Designer',
    location: 'San Francisco, CA',
    posted: 'Jan 26, 2025'
  },
  {
    company: 'Apple',
    title: 'UX/UI Designer',
    location: 'Cupertino, CA',
    posted: 'Jan 20, 2025'
  },
  {
    company: 'Netflix',
    title: 'Frontend Developer',
    location: 'Los Gatos, CA',
    posted: 'Jan 18, 2025'
  }
];

export default function Discover() {
  return (
    <div className={styles.discover}>
      <form className={styles.searchForm} onSubmit={e => e.preventDefault()}>
        <input type="text" placeholder="Job Title / Keywords" />
        <input type="text" placeholder="Location" />
        <input type="text" placeholder="Experience Level" />
        <input type="text" placeholder="Job Type" />
        <button type="submit">Search</button>
      </form>
      <div className={styles.grid}>
        {sampleJobs.map(job => (
          <JobCard key={job.title} {...job} />
        ))}
      </div>
    </div>
  );
}
