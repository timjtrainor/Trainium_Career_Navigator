import styles from './JobCard.module.css';

export default function JobCard({ company, title, location, posted }) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.logo} aria-hidden="true" />
        <div>
          <div className={styles.company}>{company}</div>
          <div className={styles.title}>{title}</div>
        </div>
      </div>
      <div className={styles.meta}>
        <span>{location}</span>
        <span>{posted}</span>
      </div>
    </div>
  );
}
