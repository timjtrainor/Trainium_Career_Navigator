# JobSpy Service

Simple FastAPI wrapper around the JobSpy scraping library. Supported job
sources are currently **Indeed** and **LinkedIn**. Additional sources can be
added by extending `PERMITTED_SOURCES` in `app/main.py`.

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JOBSPY_DELAY_SECONDS` | Seconds to wait before making each scraping request. | `1` |

The delay helps avoid triggering provider rate limits. Adjust the value in your
`.env` file if necessary.

