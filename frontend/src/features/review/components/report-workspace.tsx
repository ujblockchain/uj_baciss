import { EmptyState } from "@/components/shared/empty-state";
import { QueryBoundary } from "@/components/shared/query-boundary";
import { DecisionForm } from "@/features/review/components/decision-form";
import { DraftEditor } from "@/features/review/components/draft-editor";
import { ReportSummary } from "@/features/review/components/report-summary";
import { useReportDetail } from "@/features/review/hooks";
import { RunProgress } from "@/features/runs/components/run-progress";
import { useRunStream } from "@/features/runs/use-run-stream";

/** One report: its details and whichever decision it is waiting for. */
export const ReportWorkspace = ({ reportId }: { reportId: string }) => {
  const detail = useReportDetail(reportId);
  const run = useRunStream();

  return (
    <div className="space-y-4">
      <QueryBoundary query={detail}>
        {(data) => (
          <>
            {data.waiting_for === "review" && (
              <>
                <ReportSummary
                  reportId={reportId}
                  payload={data.pending}
                  hasPhoto={data.has_photo}
                />
                <DecisionForm
                  payload={data.pending}
                  disabled={run.state.status === "running"}
                  onDecide={(body) => {
                    void run.start(`/reports/${reportId}/review`, body);
                  }}
                />
              </>
            )}
            {data.waiting_for === "draft" && (
              <DraftEditor reportId={reportId} payload={data.pending} />
            )}
            {data.waiting_for === null && (
              <EmptyState message="This report is not waiting for a decision." />
            )}
          </>
        )}
      </QueryBoundary>
      <RunProgress run={run.state} />
    </div>
  );
};
