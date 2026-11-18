"use client";

import { PageHeader } from "@/components/shared/page-header";
import { QueryBoundary } from "@/components/shared/query-boundary";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AgentTrace } from "@/features/dashboard/components/agent-trace";
import { CountBarChart } from "@/features/dashboard/components/count-bar-chart";
import { DuplicateClusters } from "@/features/dashboard/components/duplicate-clusters";
import { UrgentTable } from "@/features/dashboard/components/urgent-table";
import { useStats } from "@/features/dashboard/hooks";

export const DashboardScreen = () => {
  const stats = useStats();

  return (
    <>
      <PageHeader title="Dashboard" description="Where reports stand right now." />
      <QueryBoundary query={stats}>
        {(data) => (
          <div className="space-y-6">
            <Card className="max-w-xs">
              <CardHeader>
                <CardTitle>Total reports</CardTitle>
              </CardHeader>
              <CardContent className="text-4xl font-semibold">{data.total}</CardContent>
            </Card>
            {data.total > 0 && (
              <div className="grid gap-6 md:grid-cols-2">
                <CountBarChart title="By status" counts={data.by_status} />
                <CountBarChart title="By category" counts={data.by_category} />
                <CountBarChart title="By department" counts={data.by_department} />
                <CountBarChart title="By urgency" counts={data.by_urgency} />
              </div>
            )}
            <UrgentTable reports={data.urgent} />
            <DuplicateClusters clusters={data.duplicate_clusters} />
          </div>
        )}
      </QueryBoundary>
      <AgentTrace />
    </>
  );
};
