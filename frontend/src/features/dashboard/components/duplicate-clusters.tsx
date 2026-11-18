import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const DuplicateClusters = ({ clusters }: { clusters: Record<string, string[]> }) => {
  const entries = Object.entries(clusters);
  return (
    <Card>
      <CardHeader>
        <CardTitle>Duplicate clusters</CardTitle>
      </CardHeader>
      <CardContent>
        {entries.length === 0 ? (
          <p className="text-sm text-muted-foreground">None.</p>
        ) : (
          <ul className="space-y-1 text-sm">
            {entries.map(([original, duplicates]) => (
              <li key={original}>
                <span className="font-medium">{original}</span> is repeated by{" "}
                {duplicates.join(", ")}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
};
