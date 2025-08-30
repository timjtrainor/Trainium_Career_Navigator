# AGENT Instructions for frontend

- This service uses Vite with React and TypeScript.
- Run `npm run dev` or `docker compose up frontend-dev` for local development with hot module reloading.
- The landing page is served from `src/` at `/` while the health check lives in `public/health/`; do not modify the health check.
- Static assets live in `public/`.
- Run `npm run build` before committing substantial changes to ensure the project compiles.
- No automated checks are defined.
