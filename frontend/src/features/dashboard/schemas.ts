import { z } from "zod";

import { reportRecordSchema } from "@/schemas/report";

const counts = z.record(z.string(), z.number());

export const statsSchema = z.object({
  total: z.number(),
  by_status: counts,
  by_category: counts,
  by_department: counts,
  by_urgency: counts,
  urgent: z.array(reportRecordSchema), // critical or high, still waiting
  duplicate_clusters: z.record(z.string(), z.array(z.string())),
});

export type Stats = z.infer<typeof statsSchema>;
