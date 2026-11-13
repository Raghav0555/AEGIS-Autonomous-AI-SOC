export default function SeverityBadge({ severity }: { severity: string }) {
  return (
    <span className={`severity severity-${severity.toLowerCase()}`}>
      <span className="severity-dot" />
      {severity}
    </span>
  );
}
