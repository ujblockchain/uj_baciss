import type { ReactNode } from "react";

import { AuthenticatedImage } from "@/components/shared/authenticated-image";
import { UrgencyBadge } from "@/components/shared/urgency-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { ReviewPayload } from "@/features/review/schemas";
import { humanize } from "@/lib/format";

const Row = ({ label, children }: { label: string; children: ReactNode }) => {
  return (
    <div className="grid gap-1 sm:grid-cols-[9rem_1fr]">
      <dt className="text-sm text-muted-foreground">{label}</dt>
      <dd className="text-sm">{children}</dd>
    </div>
  );
};

/** What the agents found out about a report, for the reviewer. */
export const ReportSummary = ({
  reportId,
  payload,
  hasPhoto,
}: {
  reportId: string;
  payload: ReviewPayload;
  hasPhoto: boolean;
}) => {
  const { triage, routing, context, duplicate } = payload;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Report {reportId}</CardTitle>
      </CardHeader>
      <CardContent>
        <dl className="space-y-3">
          <Row label="Original text">
            <p className="whitespace-pre-wrap">{payload.text}</p>
          </Row>
          {triage.language !== "en" && (
            <Row label={`Translation (${triage.language})`}>{triage.english_text}</Row>
          )}
          <Row label="Summary">{triage.summary}</Row>
          <Row label="Urgency">
            <span className="flex flex-wrap items-center gap-2">
              <UrgencyBadge urgency={triage.urgency} /> {triage.urgency_reason}
            </span>
          </Row>
          <Row label="Category">{humanize(triage.category)}</Row>
          <Row label="Routing">
            {routing.municipality}, {routing.department}. {routing.reason}
            {routing.needs_human && " A person must confirm the area."}
          </Row>
          {context && (
            <Row label="Web check">
              <p>
                {humanize(context.finding)} ({context.confidence} confidence).{" "}
                {context.summary}
              </p>
              <ul className="mt-1 list-disc pl-5">
                {context.sources.map((source) => (
                  <li key={source.url}>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline"
                    >
                      {source.title}
                    </a>
                  </li>
                ))}
              </ul>
            </Row>
          )}
          {duplicate.duplicate_of && (
            <Row label="Possible duplicate">
              Report {duplicate.duplicate_of}. {duplicate.reason}
            </Row>
          )}
          {hasPhoto && (
            <Row label="Photo">
              <AuthenticatedImage
                path={`/reports/${reportId}/photo`}
                alt={`Photo for report ${reportId}`}
              />
            </Row>
          )}
        </dl>
      </CardContent>
    </Card>
  );
};
