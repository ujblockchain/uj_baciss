import { z } from "zod";

import { categorySchema, urgencySchema } from "@/schemas/domain";

/** A saved report, as the API lists it for admins. */
export const reportRecordSchema = z.object({
  id: z.string(),
  text: z.string(),
  status: z.string(),
  category: categorySchema,
  urgency: urgencySchema,
  municipality: z.string(),
  department: z.string(),
  duplicate_of: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type ReportRecord = z.infer<typeof reportRecordSchema>;
