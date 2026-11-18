import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type { RunStep } from "@/features/runs/schemas";

type TraceValue = { steps: RunStep[]; setSteps: (steps: RunStep[]) => void };

const TraceContext = createContext<TraceValue | null>(null);

/** Remembers the steps of the latest run, for the dashboard's Agent Trace. */
export const TraceProvider = ({ children }: { children: ReactNode }) => {
  const [steps, setSteps] = useState<RunStep[]>([]);
  const value = useMemo(() => ({ steps, setSteps }), [steps]);
  return <TraceContext value={value}>{children}</TraceContext>;
};

export const useTrace = (): TraceValue => {
  const context = useContext(TraceContext);
  if (!context) throw new Error("useTrace must be used inside <TraceProvider>.");
  return context;
};
