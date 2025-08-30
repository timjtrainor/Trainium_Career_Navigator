# AGENT Instructions for frontend

- This service uses Vite with React and TypeScript.
- Run `npm run dev` or `docker compose up frontend-dev` for local development with hot module reloading.
- The landing page is served from `src/` at `/` while the health check lives in `public/health`; do not modify the health check.
- Static assets live in `public/`.
- Run `npm run build` before committing substantial changes to ensure the project compiles.

## Global conventions
- Style with Tailwind utilities or CSS modules. Tailwind breakpoints follow the defaults (`sm`, `md`, `lg`, `xl`) with container widths of `640px`, `768px`, `1024px`, and `1280px`.
- Apply `focus-visible` rings for keyboard users and keep DOM landmarks (`<header>`, `<nav>`, `<main>`). Include a skip link at the top of the page.
- Dark mode may be added later; prefer classes that work for both themes.

## Design system
- Design tokens live in `src/tokens.ts` and define color roles, spacing, radii, elevation and type ramp. Tokens export a `Tokens` type.
- Use the color roles: `bg`, `surface`, `border`, `muted`, `primary`, `info`, `success`, `warning`, `danger`.
- Reference spacing by name (`xs`, `sm`, `md`, `lg`, `xl`, `2xl`) rather than numeric indexes.

## UX and accessibility
- Left sidebar navigation groups `/jobs/*` routes under "Jobs Pipeline" and the Add Job button stays in the Jobs header so it's reachable on any jobs page.
- Debounce search (250–400ms) and sync filters with URL via `useSearchParams`.
- Fetch data with React Query; set `staleTime` for lists and show toasts for mutations.
- Modals and drawers use `role="dialog"`, focus trap, ESC to close, and `aria-labelledby`/`aria-describedby`.
- Mark the active route with `aria-current="page"` and ensure all interactive elements are keyboard accessible.
- Render persona details when present; otherwise show tallies and final decision.
- Page content begins with a heading and subheading, then any analytics/KPI cards, followed by search and filter controls before
  lists.
- List items open detail views in a right-side slide-out drawer.

## Component patterns
- Tables support sortable headers with `aria-sort`, `scope="col"` on headers, sticky header on desktop, row hover states and no row selection by default.
- Filters are controlled components with debounced search (250–400ms) and URL-synced state via `useSearchParams`.
- `DetailDrawer` and modal components trap focus and return it on close.
- `DecisionPill` uses Yes/No/— states with accessible labels and token-driven colors.
- `PersonaSnippet` and `FeedbackBox` render conditionally; submit actions show optimistic UI and a toast.
- Provide skeletons for loading, friendly empty and error states, and use the Toast system for success, error and info messages instead of console logs.

- No automated checks are defined, but add Vitest + React Testing Library tests and axe checks when introducing new features.
