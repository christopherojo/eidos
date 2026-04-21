const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function readOptionalString(value: unknown, fallback: string): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

export const env = {
  apiBaseUrl: readOptionalString(
    import.meta.env.VITE_EIDOS_API_BASE_URL,
    DEFAULT_API_BASE_URL
  ),
} as const;
