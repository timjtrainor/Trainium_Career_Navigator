# JobSpy Service

Simple FastAPI wrapper around the JobSpy scraping library. The Python package
is named `jobspy_service` to avoid clashing with the upstream library. Supported
job sources include **Indeed**, **LinkedIn**, and **Google Jobs**. Providers are
controlled via the `JOBSPY_SOURCES` allowlist environment variable.

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JOBSPY_SOURCES` | Comma-separated list of allowed providers. | `indeed,linkedin,google` |
| `JOBSPY_ENABLED` | Toggle scraping feature. | `true` |
| `JOBSPY_DELAY_SECONDS` | Seconds to wait before making each scraping request. | `2` |

The delay helps avoid triggering provider rate limits. Adjust the value in your
`.env` file if necessary.

