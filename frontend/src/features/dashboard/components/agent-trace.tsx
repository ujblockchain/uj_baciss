import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useTrace } from "@/features/runs/trace-context";
import { humanize } from "@/lib/format";

/** The agent steps of the latest run in this browser session. */
export const AgentTrace = () => {
  const { steps } = useTrace();
  return (
    <Card>
      <CardHeader>
        <CardTitle>Agent trace</CardTitle>
        <CardDescription>Steps of your latest run in this session.</CardDescription>
      </CardHeader>
      <CardContent>
        {steps.length === 0 ? (
          <p className="text-sm text-muted-foreground">No run yet in this session.</p>
        ) : (
          <ol className="space-y-1 text-sm">
            {steps.map((step, index) => (
              <li key={index}>
                <span className="font-medium">{humanize(step.node)}</span>{" "}
                <span className="text-muted-foreground">{step.message}</span>
              </li>
            ))}
          </ol>
        )}
      </CardContent>
    </Card>
  );
};
