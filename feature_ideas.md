# Feature Ideas for Trainium

## 1. UX: Quick "Dismiss" Action for Jobs

**Description**
Add a "Dismiss" or "Hide" button to the job card in the Discover feed. When clicked, the job's decision status is updated to "rejected" (or a similar negative status), and the job is immediately removed from the view if the "Hide Rejected/Bad Fit" filter is active (or by default).

**Value**
Job seekers often encounter many irrelevant postings. Currently, they have to open the job details or ignore it. A quick dismissal action allows them to rapidly curate their feed, removing noise and focusing only on relevant opportunities. This mimics the "swipe left" behavior of modern apps, improving the "triage" workflow.

**Tech Implication**
- **Frontend**: Add a "Dismiss" button/icon to the `JobsDiscoverPage` job card. Implement an API call to update the job's `decision` field to "rejected". Optimistically update the UI to remove the item from the list.
- **Backend**: Ensure the `PATCH /api/jobs/{id}` endpoint supports updating the `decision` field (it likely already does).

**Effort**
Low (Low-hanging fruit).

---

## 2. Data: Capture Salary and Job Type during Scraping

**Description**
Update the JobSpy service to capture and normalize `salary_min`, `salary_max`, and `job_type` from the scraped data. The backend `Job` model already has these fields, but the current `jobspy_service` normalization logic drops them.

**Value**
Salary and job type (Full-time, Contract, etc.) are critical decision factors. Capturing this data enables better filtering (e.g., "Show me jobs paying > $100k") and allows the AI evaluation to be more accurate (e.g., "Salary fits user expectations").

**Tech Implication**
- **JobSpy Service**: Update `Job` model in `jobspy_service` to include salary and job type fields. Update `normalize_job` function to map these fields from the raw scrape result (checking provider-specific keys like `min_amount`, `max_amount`, `job_type`). Update `_ensure_jobs_table` and SQL queries to persist these new columns.
- **Backend**: Ensure these fields are correctly receiving data (already exists in model).

**Effort**
Low/Medium (Requires DB migration/schema update in JobSpy service).

---

## 3. Search: Location-based Job Search

**Description**
Enhance the "Search" functionality to allow users to specify a location (e.g., "New York, NY", "Remote", "London"). Currently, the search only accepts a keyword and relies on default/hardcoded country settings or infers location poorly.

**Value**
Job seekers rarely search globally. They search for "Python Developer in Chicago". Adding explicit location support dramatically improves search relevance and usability.

**Tech Implication**
- **JobSpy Service**: Update `GET /jobs/search` endpoint to accept a `location` query parameter. Pass this parameter to the underlying `scrape_jobs` library function (which supports it).
- **Frontend**: Add a "Location" input field next to the "Search" bar in `JobsDiscoverPage`. Pass the value to the API.

**Effort**
Low (Low-hanging fruit).
