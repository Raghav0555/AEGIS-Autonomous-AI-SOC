"use client";

import { useEffect, useState } from "react";
import {
  checkBackendHealth,
  fetchEvents,
  fetchIncidents,
} from "@/lib/api";

const stats = [
  {
    label: "Security Events",
    value: "1,284",
    change: "+12.5%",
    status: "neutral",
  },
  {
    label: "Active Incidents",
    value: "24",
    change: "+4",
    status: "warning",
  },
  {
    label: "Critical Threats",
    value: "3",
    change: "-2",
    status: "critical",
  },
  {
    label: "Systems Monitored",
    value: "148",
    change: "100%",
    status: "success",
  },
];

const events = [
  {
    time: "10:42:18",
    event: "Multiple failed login attempts",
    source: "AUTH",
    user: "admin",
    ip: "185.10.20.30",
    severity: "HIGH",
  },
  {
    time: "10:41:52",
    event: "New privileged session",
    source: "AUTH",
    user: "admin",
    ip: "185.10.20.30",
    severity: "HIGH",
  },
  {
    time: "10:39:11",
    event: "Large outbound data transfer",
    source: "HTTP",
    user: "admin",
    ip: "185.10.20.30",
    severity: "CRITICAL",
  },
  {
    time: "10:36:44",
    event: "Successful user authentication",
    source: "AUTH",
    user: "rahul",
    ip: "10.0.0.15",
    severity: "LOW",
  },
  {
    time: "10:34:27",
    event: "Suspicious request frequency",
    source: "HTTP",
    user: "service-api",
    ip: "10.0.2.42",
    severity: "MEDIUM",
  },
];

const fallbackIncidents: Incident[] = [
  {
    incident_id: "INC-024",
    incident_type: "Potential account compromise",
    severity: "critical",
    events: ["EVT-101", "EVT-102", "EVT-103"],
    confidence: 0.94,
    affected_users: ["admin"],
    source_ips: ["185.10.20.30"],
    created_at: "2026-10-01T10:42:18Z",
  },
  {
    incident_id: "INC-023",
    incident_type: "Brute-force authentication attempt",
    severity: "high",
    events: ["EVT-104", "EVT-105", "EVT-106"],
    confidence: 0.91,
    affected_users: ["admin"],
    source_ips: ["185.10.20.30"],
    created_at: "2026-10-01T10:41:52Z",
  },
  {
    incident_id: "INC-022",
    incident_type: "Unusual privileged activity",
    severity: "high",
    events: ["EVT-107", "EVT-108"],
    confidence: 0.86,
    affected_users: ["admin"],
    source_ips: ["10.0.0.15"],
    created_at: "2026-10-01T10:39:11Z",
  },
];

const detectionRules = [
  {
    name: "BRUTE_FORCE",
    description: "Detects excessive failed authentication attempts.",
    triggered: 14,
    severity: "HIGH",
    status: "Active",
  },
  {
    name: "NEW_PRIVILEGED_SESSION",
    description: "Detects privileged activity from an unseen IP.",
    triggered: 6,
    severity: "HIGH",
    status: "Active",
  },
  {
    name: "POTENTIAL_EXFILTRATION",
    description:
      "Detects sensitive access followed by large data transfer.",
    triggered: 3,
    severity: "CRITICAL",
    status: "Active",
  },
];
type SecurityEvent = {
  event_id: string;
  timestamp: string;
  event_type: string;
  source: string;
  user: string | null;
  ip: string | null;
  severity: "low" | "medium" | "high" | "critical";
  metadata: Record<string, unknown>;
};
type Incident = {
  incident_id: string;
  severity: "low" | "medium" | "high" | "critical";
  confidence: number;
  incident_type: string;
  affected_users: string[];
  source_ips: string[];
  events: string[];
  created_at: string;
};
type Detection = {
  rule: string;
  severity: "low" | "medium" | "high" | "critical";
  reason: string;
};
const formatConfidence = (confidence: number) =>
  `${Math.round(confidence * 100)}%`;

const getIncidentStatus = (incident: Incident) =>
  incident.events.length > 2 ? "Investigating" : "Contained";

function SeverityBadge({ severity }: { severity: string }) {
  return (
    <span className={`severity severity-${severity.toLowerCase()}`}>
      <span className="severity-dot" />
      {severity}
    </span>
  );
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<
    "checking" | "online" | "offline"
  >("checking");

  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(
    null,
  );
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>(fallbackIncidents);
  const [incidentsLoading, setIncidentsLoading] = useState(true);
  const [incidentsError, setIncidentsError] = useState<string | null>(null);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [eventsError, setEventsError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    const loadEvents = async () => {
      try {
        setEventsLoading(true);
        setEventsError(null);

        const data = await fetchEvents();

        if (mounted) {
          setEvents(data);
        }
      } catch {
        if (mounted) {
          setEventsError("Unable to load security events");
        }
      } finally {
        if (mounted) {
          setEventsLoading(false);
        }
      }
    };

    loadEvents();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    const loadIncidents = async () => {
      try {
        setIncidentsLoading(true);
        setIncidentsError(null);

        const data = await fetchIncidents();

        if (mounted) {
          setIncidents(Array.isArray(data) ? (data as Incident[]) : fallbackIncidents);
        }
      } catch {
        if (mounted) {
          setIncidentsError("Unable to load security incidents");
          setIncidents(fallbackIncidents);
        }
      } finally {
        if (mounted) {
          setIncidentsLoading(false);
        }
      }
    };

    loadIncidents();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    const checkHealth = async () => {
      try {
        await checkBackendHealth();

        if (mounted) {
          setBackendStatus("online");
        }
      } catch {
        if (mounted) {
          setBackendStatus("offline");
        }
      }
    };

    checkHealth();

    return () => {
      mounted = false;
    };
  }, []);

  return (
    <main className="soc-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">A</div>

          <div>
            <div className="brand-name">AEGIS</div>
            <div className="brand-subtitle">AUTONOMOUS SOC</div>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-section">OPERATIONS</div>

          <a className="nav-item active" href="#">
            <span>⌂</span>
            Dashboard
          </a>

          <a className="nav-item" href="#">
            <span>◈</span>
            Incidents
            <span className="nav-count">24</span>
          </a>

          <a className="nav-item" href="#">
            <span>⌁</span>
            Security Events
          </a>

          <a className="nav-item" href="#">
            <span>◌</span>
            Attack Timeline
          </a>

          <div className="nav-section">ANALYSIS</div>

          <a className="nav-item" href="#">
            <span>✦</span>
            AI Investigation
          </a>

          <a className="nav-item" href="#">
            <span>◇</span>
            Detection Rules
          </a>

          <div className="nav-section">SYSTEM</div>

          <a className="nav-item" href="#">
            <span>◉</span>
            Data Sources
          </a>

          <a className="nav-item" href="#">
            <span>⚙</span>
            Settings
          </a>
        </nav>

        {/* System status belongs INSIDE the sidebar */}
        <div className="sidebar-footer">
          <div className="system-status">
            <span
              className={`status-pulse ${
                backendStatus === "online"
                  ? "status-online"
                  : backendStatus === "offline"
                    ? "status-offline"
                    : "status-checking"
              }`}
            />

            <div>
              <strong>
                {backendStatus === "online"
                  ? "System Operational"
                  : backendStatus === "offline"
                    ? "Backend Offline"
                    : "Checking System..."}
              </strong>

              <small>
                {backendStatus === "online"
                  ? "All services healthy"
                  : backendStatus === "offline"
                    ? "Backend connection unavailable"
                    : "Connecting to backend..."}
              </small>
            </div>
          </div>

          <div className="version">AEGIS v0.1.0</div>
        </div>
      </aside>

      <section className="dashboard">
        <header className="topbar">
          <div>
            <div className="breadcrumb">
              SECURITY OPERATIONS / OVERVIEW
            </div>
            <h1>Security Operations Center</h1>
          </div>

          <div className="topbar-actions">
            <div className="live-indicator">
              <span />
              LIVE
            </div>

            <button
              className="icon-button"
              aria-label="Notifications"
            >
              ◇
            </button>

            <div className="operator">
              <div className="avatar">RS</div>

              <div>
                <strong>Operator</strong>
                <small>Administrator</small>
              </div>
            </div>
          </div>
        </header>

        <div className="dashboard-content">
          <section className="stats-grid">
            {stats.map((stat) => (
              <div className="stat-card" key={stat.label}>
                <div className="stat-header">
                  <span>{stat.label}</span>
                  <span
                    className={`stat-indicator ${stat.status}`}
                  />
                </div>

                <div className="stat-value">{stat.value}</div>

                <div className="stat-change">
                  <span>{stat.change}</span>
                  <span>vs previous period</span>
                </div>
              </div>
            ))}
          </section>

          <section className="overview-grid">
            <div className="panel threat-panel">
              <div className="panel-header">
                <div>
                  <div className="panel-eyebrow">
                    THREAT OVERVIEW
                  </div>
                  <h2>Detection Activity</h2>
                </div>

                <select defaultValue="24h">
                  <option value="24h">Last 24 hours</option>
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                </select>
              </div>

              <div className="threat-chart">
                <div className="chart-y-axis">
                  <span>80</span>
                  <span>60</span>
                  <span>40</span>
                  <span>20</span>
                  <span>0</span>
                </div>

                <div className="chart-area">
                  <div className="chart-grid" />

                  <svg
                    className="chart-line"
                    viewBox="0 0 700 220"
                    preserveAspectRatio="none"
                  >
                    <defs>
                      <linearGradient
                        id="areaGradient"
                        x1="0"
                        x2="0"
                        y1="0"
                        y2="1"
                      >
                        <stop
                          offset="0%"
                          stopColor="rgba(56, 189, 248, 0.25)"
                        />
                        <stop
                          offset="100%"
                          stopColor="rgba(56, 189, 248, 0)"
                        />
                      </linearGradient>
                    </defs>

                    <path
                      d="M0 178 C45 170 60 160 95 166 C130 172 145 130 185 138 C220 145 230 112 270 126 C310 140 330 92 370 110 C410 128 430 68 470 82 C510 96 525 55 565 74 C605 93 625 42 660 58 C680 67 690 48 700 43 L700 220 L0 220 Z"
                      fill="url(#areaGradient)"
                    />

                    <path
                      d="M0 178 C45 170 60 160 95 166 C130 172 145 130 185 138 C220 145 230 112 270 126 C310 140 330 92 370 110 C410 128 430 68 470 82 C510 96 525 55 565 74 C605 93 625 42 660 58 C680 67 690 48 700 43"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      vectorEffect="non-scaling-stroke"
                    />
                  </svg>

                  <div className="chart-labels">
                    <span>00:00</span>
                    <span>06:00</span>
                    <span>12:00</span>
                    <span>18:00</span>
                    <span>NOW</span>
                  </div>
                </div>
              </div>

              <div className="chart-legend">
                <span>
                  <i className="legend-dot events" />
                  Events detected
                </span>

                <span>
                  <i className="legend-dot threats" />
                  Threats detected
                </span>
              </div>
            </div>

            <div className="panel severity-panel">
              <div className="panel-header">
                <div>
                  <div className="panel-eyebrow">
                    CURRENT STATE
                  </div>
                  <h2>Severity Distribution</h2>
                </div>
              </div>

              <div className="severity-total">
                <strong>1,284</strong>
                <span>Total events</span>
              </div>

              <div className="severity-bars">
                <div className="severity-row">
                  <div>
                    <span className="severity-label critical-text">
                      Critical
                    </span>
                    <span>3 events</span>
                  </div>

                  <div className="bar">
                    <i style={{ width: "8%" }} />
                  </div>
                </div>

                <div className="severity-row">
                  <div>
                    <span className="severity-label high-text">
                      High
                    </span>
                    <span>24 events</span>
                  </div>

                  <div className="bar">
                    <i style={{ width: "24%" }} />
                  </div>
                </div>

                <div className="severity-row">
                  <div>
                    <span className="severity-label medium-text">
                      Medium
                    </span>
                    <span>86 events</span>
                  </div>

                  <div className="bar">
                    <i style={{ width: "48%" }} />
                  </div>
                </div>

                <div className="severity-row">
                  <div>
                    <span className="severity-label low-text">
                      Low
                    </span>
                    <span>1,171 events</span>
                  </div>

                  <div className="bar">
                    <i style={{ width: "92%" }} />
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="lower-grid">
            <div className="panel events-panel">
              <div className="panel-header">
                <div>
                  <div className="panel-eyebrow">
                    EVENT STREAM
                  </div>
                  <h2>Recent Security Events</h2>
                </div>

                <button className="view-button">
                  View all →
                </button>
              </div>

              <div className="event-table">
                <div className="event-row event-header">
                  <span>TIME</span>
                  <span>EVENT</span>
                  <span>SOURCE</span>
                  <span>USER / IP</span>
                  <span>SEVERITY</span>
                </div>
              {eventsLoading ? (
                <div className="event-empty-state">Loading security events...</div>
              ) : eventsError ? (
                <div className="event-empty-state">{eventsError}</div>
              ) : (
                events.map((event) => (
                  <div
                    className="event-row"
                    key={event.event_id}
                  >
                    <span className="event-time">
                      {new Date(event.timestamp).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                      })} 
                    </span>

                    <span className="event-name">
                      <span className="event-icon">↗</span>
                      {event.event_type}
                    </span>

                    <span className="source-tag">
                      {event.source}
                    </span>

                    <span className="event-user">
                      {event.user}
                      <small>{event.ip}</small>
                    </span>

                    <SeverityBadge severity={event.severity} />
                  </div>
                ))
              )}
              </div>
            </div>

            <div className="panel incidents-panel">
              <div className="panel-header">
                <div>
                  <div className="panel-eyebrow">
                    INCIDENT RESPONSE
                  </div>
                  <h2>Active Incidents</h2>
                </div>

                <button className="view-button">
                  View all →
                </button>
              </div>

              <div className="incident-list">
                {incidentsLoading ? (
                  <div className="event-empty-state">Loading incidents...</div>
                ) : incidentsError ? (
                  <div className="event-empty-state">{incidentsError}</div>
                ) : (
                  incidents.map((incident) => (
                    <div
                      className="incident-card"
                      key={incident.incident_id}
                      onClick={() => setSelectedIncident(incident)}
                    >
                      <div className="incident-top">
                        <span className="incident-id">
                          {incident.incident_id}
                        </span>

                        <SeverityBadge
                          severity={incident.severity}
                        />
                      </div>

                      <h3>{incident.incident_type}</h3>

                      <div className="incident-meta">
                        <span>{incident.events.length} events</span>
                        <span>
                          Confidence {formatConfidence(incident.confidence)}
                        </span>
                      </div>

                      <div className="incident-bottom">
                        <span className="incident-status">
                          <i />
                          {getIncidentStatus(incident)}
                        </span>

                        <span className="incident-arrow">→</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </section>

          <section className="panel rules-panel">
            <div className="panel-header">
              <div>
                <div className="panel-eyebrow">
                  DETECTION ENGINE
                </div>
                <h2>Detection Rules</h2>
              </div>

              <span className="rules-active">
                <i />
                3 rules active
              </span>
            </div>

            <div className="rules-grid">
              {detectionRules.map((rule) => (
                <div className="rule-card" key={rule.name}>
                  <div className="rule-top">
                    <span className="rule-name">
                      {rule.name}
                    </span>

                    <SeverityBadge
                      severity={rule.severity}
                    />
                  </div>

                  <p>{rule.description}</p>

                  <div className="rule-bottom">
                    <span>
                      <strong>{rule.triggered}</strong>{" "}
                      triggered
                    </span>

                    <span className="rule-status">
                      <i />
                      {rule.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>

        {selectedIncident && (
          <div
            className="incident-overlay"
            onClick={() => setSelectedIncident(null)}
          >
            <aside
              className="incident-drawer"
              onClick={(event) => event.stopPropagation()}
            >
              <div className="drawer-header">
                <div>
                  <div className="panel-eyebrow">
                    INCIDENT DETAILS
                  </div>
                  <span className="drawer-id">
                    {selectedIncident.incident_id}
                  </span>
                </div>

                <button
                  className="drawer-close"
                  onClick={() => setSelectedIncident(null)}
                  aria-label="Close incident details"
                >
                  ×
                </button>
              </div>

              <div className="drawer-content">
                <div className="drawer-title-row">
                  <h2>{selectedIncident.incident_type}</h2>

                  <SeverityBadge
                    severity={selectedIncident.severity}
                  />
                </div>

                <div className="drawer-status">
                  <span className="incident-status">
                    <i />
                    {getIncidentStatus(selectedIncident)}
                  </span>
                </div>

                <div className="drawer-stats">
                  <div>
                    <span>CONFIDENCE</span>
                    <strong>
                      {formatConfidence(selectedIncident.confidence)}
                    </strong>
                  </div>

                  <div>
                    <span>RELATED EVENTS</span>
                    <strong>{selectedIncident.events.length}</strong>
                  </div>
                </div>

                <div className="drawer-section">
                  <div className="drawer-section-title">
                    AFFECTED USER
                  </div>

                  <div className="drawer-value">
                    {selectedIncident.affected_users[0] ?? "Unknown"}
                  </div>
                </div>

                <div className="drawer-section">
                  <div className="drawer-section-title">
                    SOURCE IP
                  </div>

                  <div className="drawer-value drawer-code">
                    {selectedIncident.source_ips[0] ?? "Unknown"}
                  </div>
                </div>

                <div className="drawer-section">
                  <div className="drawer-section-title">
                    RELATED ACTIVITY
                  </div>

                  <div className="activity-list">
                    {selectedIncident.events.slice(0, 3).map((eventId) => (
                      <div key={eventId} className="activity-item">
                        <span />
                        {eventId}
                      </div>
                    ))}
                  </div>
                </div>

                <button className="investigate-button">
                  Begin AI Investigation
                  <span>→</span>
                </button>
              </div>
            </aside>
          </div>
        )}
      </section>
    </main>
  );
}