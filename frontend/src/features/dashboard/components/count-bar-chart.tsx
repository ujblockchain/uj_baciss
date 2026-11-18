import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import { humanize } from "@/lib/format";

const config = { count: { label: "Reports", color: "var(--chart-1)" } } satisfies ChartConfig;

/** One bar chart of counts, used for every breakdown on the dashboard. */
export const CountBarChart = ({
  title,
  counts,
}: {
  title: string;
  counts: Record<string, number>;
}) => {
  const data = Object.entries(counts).map(([name, count]) => ({
    name: humanize(name),
    count,
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer config={config} className="h-56 w-full">
          <BarChart data={data} accessibilityLayer>
            <CartesianGrid vertical={false} />
            <XAxis dataKey="name" tickLine={false} axisLine={false} tickMargin={8} />
            <YAxis allowDecimals={false} width={28} tickLine={false} axisLine={false} />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Bar dataKey="count" fill="var(--color-count)" radius={4} />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
};
