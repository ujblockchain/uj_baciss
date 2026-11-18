import { useCallback, useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { ApiError } from "@/lib/api-client";
import { queryKeys } from "@/lib/query-keys";
import { streamEvents } from "@/lib/sse";
import { runEventSchema, type RunStep } from "@/features/runs/schemas";
import { useTrace } from "@/features/runs/trace-context";

export type RunStatus = "idle" | "running" | "paused" | "done" | "error";

export type RunState = {
  status: RunStatus;
  reportId: string | null;
  steps: RunStep[];
  error: string | null;
};

const IDLE: RunState = { status: "idle", reportId: null, steps: [], error: null };

/** Runs a streamed request (submit a report, send a review) and tracks its steps. */
export const useRunStream = () => {
  const queryClient = useQueryClient();
  const { setSteps } = useTrace();
  const [state, setState] = useState<RunState>(IDLE);
  const controller = useRef<AbortController | null>(null);

  useEffect(() => () => controller.current?.abort(), []);

  const start = useCallback(
    async (path: string, body: unknown): Promise<RunState> => {
      controller.current?.abort();
      const abort = new AbortController();
      controller.current = abort;

      let current: RunState = { ...IDLE, status: "running" };
      const update = (changes: Partial<RunState>) => {
        current = { ...current, ...changes };
        setState(current);
      };
      update({});

      try {
        for await (const raw of streamEvents(path, body, abort.signal)) {
          const event = runEventSchema.parse(raw);
          switch (event.event) {
            case "started":
              update({ reportId: event.data.report_id });
              break;
            case "step":
              update({ steps: [...current.steps, event.data] });
              break;
            case "paused":
              update({ status: "paused" });
              break;
            case "done":
              update({ status: "done" });
              break;
            case "error":
              update({ status: "error", error: event.data.message });
              break;
          }
        }
        if (current.status === "running") update({ status: "done" });
      } catch (error) {
        if (!abort.signal.aborted) {
          const message =
            error instanceof ApiError ? error.message : "The connection was lost.";
          update({ status: "error", error: message });
        }
      }

      setSteps(current.steps);
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: queryKeys.myReports }),
        queryClient.invalidateQueries({ queryKey: queryKeys.review }),
      ]);
      return current;
    },
    [queryClient, setSteps],
  );

  const reset = useCallback(() => setState(IDLE), []);

  return { state, start, reset };
};
