# Personas Catalog

The personas catalog defines how Trainium tailors analysis and decisions.
Entries live in `backend/config/personas.yml` and are exposed via the
`/api/personas` endpoint.

## Usage
- Fetch all personas: `GET /api/personas`.
- Compose personas by category, e.g., `Recruiter + Builder + Judge`.
- Each persona produces a boolean `recommend` decision with a rationale.

Personas are grouped into advisory, motivational, and decision categories.
