import { UrgencyBadge } from "@/components/shared/urgency-badge";
import { formatDateTime, humanize } from "@/lib/format";
import { cn } from "@/lib/utils";
import type { ReportRecord } from "@/schemas/report";

type Props = {
  reports: ReportRecord[];
  selectedId: string | null;
  onSelect: (id: string) => void;
};

/** The reports waiting for a decision, most urgent first (the API sorts them). */
export const QueueList = ({ reports, selectedId, onSelect }: Props) => {
  return (
    <ul className="space-y-2" aria-label="Review queue">
      {reports.map((report) => (
        <li key={report.id}>
          <button
            type="button"
            onClick={() => onSelect(report.id)}
            aria-current={report.id === selectedId}
            className={cn(
              "w-full rounded-lg border bg-card p-3 text-left text-sm transition-colors hover:bg-muted",
              report.id === selectedId && "border-primary bg-muted",
            )}
          >
            <div className="flex items-center justify-between gap-2">
              <span className="font-medium">{humanize(report.category)}</span>
              <UrgencyBadge urgency={report.urgency} />
            </div>
            <p className="mt-1 line-clamp-2 text-muted-foreground">{report.text}</p>
            <p className="mt-1 text-xs text-muted-foreground">
              {report.id} · {humanize(report.status)} · {formatDateTime(report.created_at)}
            </p>
          </button>
        </li>
      ))}
    </ul>
  );
};
