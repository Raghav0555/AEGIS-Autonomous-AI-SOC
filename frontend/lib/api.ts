const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function requestJson<T>(
  path: string,
  errorMessage: string,
  init: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    cache: "no-store",
    ...init,
  });

  if (!response.ok) {
    throw new Error(errorMessage);
  }

  return response.json();
}

export function checkBackendHealth() {
  return requestJson<{ status: string; service: string }>(
    "/api/health",
    "Backend health check failed",
  );
}

export function fetchEvents() {
  return requestJson<unknown[]>(
    "/api/events",
    "Failed to fetch security events",
  );
}

export function fetchIncidents() {
  return requestJson<unknown[]>(
    "/api/incidents",
    "Failed to fetch incidents",
  );
}

export function runDetection() {
  return requestJson<{
    events_analyzed: number;
    alerts_generated: number;
    alerts: unknown[];
  }>("/api/detection/run", "Failed to run detection", { method: "POST" });
}
