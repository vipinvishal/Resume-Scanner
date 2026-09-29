import type { Status } from '../lib/demo'
export function StatusBadge({ status }: { status: Status }) {
  const label = status === 'NOT_EVIDENCED' ? 'Not evidenced' : status[0] + status.slice(1).toLowerCase()
  return <span className={`status status-${status.toLowerCase()}`}>{label}</span>
}
