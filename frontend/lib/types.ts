export type Severity = "low" | "medium" | "high" | "critical";

export type SecurityEvent = {
  event_id: string;
  timestamp: string;
  event_type: string;
  source: string;
  user: string | null;
  ip: string | null;
  severity: Severity;
  metadata: Record<string, unknown>;
};

export type Incident = {
  incident_id: string;
  severity: Severity;
  confidence: number;
  incident_type: string;
  affected_users: string[];
  source_ips: string[];
  events: string[];
  created_at: string;
};

export type Detection = {
  rule: string;
  severity: Severity;
  reason: string;
};
