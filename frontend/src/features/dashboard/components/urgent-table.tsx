import { UrgencyBadge } from "@/components/shared/urgency-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { humanize } from "@/lib/format";
import type { ReportRecord } from "@/schemas/report";

export const UrgentTable = ({ reports }: { reports: ReportRecord[] }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Urgent, still waiting</CardTitle>
      </CardHeader>
      <CardContent>
        {reports.length === 0 ? (
          <p className="text-sm text-muted-foreground">None.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Report</TableHead>
                <TableHead>Urgency</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {reports.map((report) => (
                <TableRow key={report.id}>
                  <TableCell className="font-medium">{report.id}</TableCell>
                  <TableCell>
                    <UrgencyBadge urgency={report.urgency} />
                  </TableCell>
                  <TableCell>{humanize(report.category)}</TableCell>
                  <TableCell>{report.department}</TableCell>
                  <TableCell>{humanize(report.status)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
};
