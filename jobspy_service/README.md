# JobSpy Service

Simple FastAPI wrapper around the JobSpy scraping library. The Python package
is named `jobspy_service` to avoid clashing with the upstream library. Supported
job sources include **Indeed**, **LinkedIn**, and **Google Jobs**. Providers are
controlled via the `JOBSPY_SOURCES` allowlist environment variable.

## Normalized job schema

The `/jobs/search` endpoint returns jobs using a consistent JSON structure
regardless of the upstream source. Each job contains the following fields:

| Field          | Description                  |
|----------------|------------------------------|
| `title`        | Title of the position        |
| `company`      | Company offering the role    |
| `description`  | Short description of the job |
| `location`     | Location of the role         |
| `url`          | Link to the job posting      |
| `remote_status`| Remote/onsite status         |

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JOBSPY_SOURCES` | Comma-separated list of allowed providers. | `indeed,linkedin,google` |
| `JOBSPY_ENABLED` | Toggle scraping feature. | `true` |
| `JOBSPY_DELAY_SECONDS` | Seconds to wait before making each scraping request. | `2` |
| `JOBSPY_CACHE_TTL_SECONDS` | Seconds to cache job search results. | `600` |
| `BIG_COMPANY_THRESHOLD` | Similarity cutoff for large companies during deduping. | `0.9` |
| `SMALL_COMPANY_THRESHOLD` | Similarity cutoff for small companies during deduping. | `0.85` |

The delay helps avoid triggering provider rate limits. Adjust the value in your
`.env` file if necessary. Recent search results are cached in-memory for the
configured TTL to speed up repeat queries.

