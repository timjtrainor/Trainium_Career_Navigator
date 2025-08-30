# AGENT Instructions for frontend

- This service uses Vite with React and TypeScript.
- Run `npm run dev` or `docker compose up frontend-dev` for local development with hot module reloading.
- The landing page is served from `src/` at `/` while the health check lives in `public/health`; do not modify the health check.
- Static assets live in `public/`.
- Run `npm run build` before committing substantial changes to ensure the project compiles.

## Design system
- Design tokens live in `src/tokens.ts` and define color roles, spacing, radii, elevation and type ramp. Tokens export a `Tokens` type.
- Style with Tailwind utilities or CSS modules; keep focus rings visible.
- Use the color roles: `bg`, `surface`, `border`, `muted`, `primary`, `info`, `success`, `warning`, `danger`.
- Reference spacing by name (`xs`, `sm`, `md`, `lg`, `xl`, `2xl`) rather than numeric indexes.

## UX and accessibility
- Top navigation with `/jobs/*` sub-nav and persistent “Add Job” button.
- Debounce search (250–400ms) and sync filters with URL via `useSearchParams`.
- Fetch data with React Query; set `staleTime` for lists and show toasts for mutations.
- Modals and drawers use `role="dialog"`, focus trap, ESC to close, and `aria-labelledby`/`aria-describedby`.
- Mark the active route with `aria-current="page"` and include a skip link.
- Render persona details when present; otherwise show tallies and final decision.

## Component patterns
- Tables support sortable headers with `aria-sort` and sticky headers on desktop.
- Decision pills use Yes/No/— states with accessible labels and color roles.
- Provide empty, loading and error states with skeletons to avoid flicker.
- Use the Toast component for success, error and info messages instead of console logs.

- No automated checks are defined, but add Vitest + React Testing Library tests and axe checks when introducing new features.
