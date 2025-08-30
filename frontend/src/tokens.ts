export const tokens = {
  color: {
    bg: "#ffffff",
    surface: "#f5f5f5",
    border: "#e0e0e0",
    muted: "#6b7280",
    primary: "#2563eb",
    info: "#0ea5e9",
    success: "#16a34a",
    warning: "#f59e0b",
    danger: "#dc2626"
  },
  spacing: {
    none: 0,
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    "2xl": 32
  },
  radii: { none: 0, sm: 6, md: 12, lg: 16, xl: 20 },
  elevation: {
    sm: "0 1px 2px rgba(0,0,0,0.05)",
    md: "0 4px 6px rgba(0,0,0,0.1)",
    lg: "0 10px 15px rgba(0,0,0,0.15)"
  },
  typography: {
    xs: "0.75rem",
    sm: "0.875rem",
    base: "1rem",
    md: "1.125rem",
    lg: "1.25rem",
    xl: "1.5rem",
    "2xl": "2rem",
    "3xl": "2.5rem"
  }
} as const;

export type Tokens = typeof tokens;
