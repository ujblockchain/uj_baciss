"use client";

import { PageHeader } from "@/components/shared/page-header";
import { QueryBoundary } from "@/components/shared/query-boundary";
import { MyReportCard } from "@/features/reports/components/my-report-card";
import { useMyReports } from "@/features/reports/hooks";

export const MyReportsScreen = () => {
  const reports = useMyReports();

  return (
    <>
      <PageHeader
        title="My reports"
        description="Follow each report and read the reply when it is ready."
      />
      <QueryBoundary
        query={reports}
        isEmpty={(data) => data.length === 0}
        emptyMessage="You have not submitted a report yet."
      >
        {(data) => (
          <div className="space-y-4">
            {data.map((report) => (
              <MyReportCard key={report.id} report={report} />
            ))}
          </div>
        )}
      </QueryBoundary>
    </>
  );
};
