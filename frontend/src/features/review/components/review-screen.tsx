"use client";

import { useState } from "react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { QueryBoundary } from "@/components/shared/query-boundary";
import { QueueList } from "@/features/review/components/queue-list";
import { ReportWorkspace } from "@/features/review/components/report-workspace";
import { useReviewQueue } from "@/features/review/hooks";

export const ReviewScreen = () => {
  const queue = useReviewQueue();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  // A finished report leaves the queue; then nothing is selected.
  const activeId = queue.data?.some((r) => r.id === selectedId) ? selectedId : null;

  return (
    <>
      <PageHeader
        title="Review queue"
        description="Reports and drafted replies waiting for your decision, most urgent first."
      />
      <div className="grid gap-6 lg:grid-cols-[22rem_1fr]">
        <QueryBoundary
          query={queue}
          isEmpty={(reports) => reports.length === 0}
          emptyMessage="Nothing is waiting for review."
        >
          {(reports) => (
            <QueueList reports={reports} selectedId={activeId} onSelect={setSelectedId} />
          )}
        </QueryBoundary>
        <section aria-label="Selected report">
          {activeId ? (
            <ReportWorkspace key={activeId} reportId={activeId} />
          ) : (
            <EmptyState message="Select a report to review it." />
          )}
        </section>
      </div>
    </>
  );
};
