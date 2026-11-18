import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, FieldLabel } from "@/components/ui/field";
import { Textarea } from "@/components/ui/textarea";
import { useDraftDecision } from "@/features/review/hooks";
import type { DraftPayload } from "@/features/review/schemas";

/** The second approval: read the drafted reply, edit it if needed, then decide. */
export const DraftEditor = ({
  reportId,
  payload,
}: {
  reportId: string;
  payload: DraftPayload;
}) => {
  const original = payload.draft.body;
  const [text, setText] = useState(original);
  const decision = useDraftDecision(reportId);

  const decide = (action: "approve" | "reject") =>
    decision.mutate(
      { action, ...(action === "approve" && text !== original && { text }) },
      {
        onSuccess: (result) => toast.success(`Report ${reportId}: ${result.status}`),
        onError: (error) => toast.error(error.message),
      },
    );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Draft reply</CardTitle>
        <CardDescription>
          From {payload.department}. The citizen sees this reply once you approve it.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Field>
          <FieldLabel htmlFor="draft">Reply to the citizen</FieldLabel>
          <Textarea
            id="draft"
            rows={12}
            value={text}
            onChange={(event) => setText(event.target.value)}
          />
        </Field>
        {payload.draft.policy_sources.length > 0 && (
          <p className="text-sm text-muted-foreground">
            Based on: {payload.draft.policy_sources.join(", ")}
          </p>
        )}
        <div className="flex gap-2">
          <Button disabled={decision.isPending} onClick={() => decide("approve")}>
            Approve
          </Button>
          <Button
            variant="outline"
            disabled={decision.isPending}
            onClick={() => decide("reject")}
          >
            Reject
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
