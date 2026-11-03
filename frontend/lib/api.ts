const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function checkBackendHealth(): Promise<{
  status: string;
  service: string;
}> {
  const response = await fetch(`${API_URL}/api/health`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function fetchEvents(): Promise<unknown[]> {
  const response = await fetch(`${API_URL}/api/events`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch security events");
  }

  return response.json();
}

export async function fetchIncidents(): Promise<unknown[]> {
  const response = await fetch(`${API_URL}/api/incidents`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch incidents");
  }

  return response.json();
}