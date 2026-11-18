import { AuthenticatedImage } from "@/components/shared/authenticated-image";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { StageBadge } from "@/features/reports/components/stage-badge";
import type { MyReport } from "@/features/reports/schemas";
import { formatDateTime } from "@/lib/format";

export const MyReportCard = ({ report }: { report: MyReport }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex flex-wrap items-center justify-between gap-2">
          <span>Report {report.id}</span>
          <StageBadge status={report.status} stage={report.stage} />
        </CardTitle>
        <CardDescription>{formatDateTime(report.created_at)}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="whitespace-pre-wrap">{report.text}</p>
        {report.has_photo && (
          <AuthenticatedImage
            path={`/reports/${report.id}/photo`}
            alt={`Photo for report ${report.id}`}
          />
        )}
        {report.reply && (
          <div className="rounded-lg bg-muted p-4">
            <p className="mb-1 text-sm font-medium">Reply</p>
            <p className="whitespace-pre-wrap text-sm">{report.reply}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
