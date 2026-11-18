import { CircleCheckIcon, Loader2Icon, OctagonXIcon } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { humanize } from "@/lib/format";
import type { RunState } from "@/features/runs/use-run-stream";

const TITLE = {
  running: "Working…",
  paused: "Waiting for the next decision",
  done: "Finished",
  error: "Something went wrong",
} as const;

/** The live list of agent steps for a streamed run. */
export const RunProgress = ({ run }: { run: RunState }) => {
  if (run.status === "idle") return null;

  return (
    <Card aria-live="polite">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {run.status === "running" && <Loader2Icon className="size-4 animate-spin" />}
          {run.status === "error" ? (
            <OctagonXIcon className="size-4 text-destructive" />
          ) : (
            run.status !== "running" && <CircleCheckIcon className="size-4" />
          )}
          {TITLE[run.status]}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="space-y-1 text-sm">
          {run.steps.map((step, index) => (
            <li key={index} className="flex gap-2">
              <span className="font-medium">{humanize(step.node)}</span>
              <span className="text-muted-foreground">{step.message}</span>
            </li>
          ))}
        </ol>
        {run.error && <p className="mt-2 text-sm text-destructive">{run.error}</p>}
      </CardContent>
    </Card>
  );
};
