import { z } from "zod";

export const sampleSchema = z.object({
  id: z.string(),
  language: z.string(),
  text: z.string(),
});

export const transcriptSchema = z.object({ text: z.string(), warning: z.string() });

export const myReportSchema = z.object({
  id: z.string(),
  text: z.string(),
  status: z.string(),
  stage: z.string(), // the status in plain words, from the API
  reply: z.string().nullable(), // the approved reply, once there is one
  created_at: z.string(),
  has_photo: z.boolean(),
});

export const photoOutcomeSchema = z.object({ report_id: z.string(), size: z.number() });

/** Same limits as the API's ReportIn. */
export const submitSchema = z.object({
  text: z
    .string()
    .trim()
    .min(5, "Describe the problem in at least 5 characters.")
    .max(2000, "Keep the report under 2000 characters."),
});

export type Sample = z.infer<typeof sampleSchema>;
export type MyReport = z.infer<typeof myReportSchema>;
export type SubmitValues = z.infer<typeof submitSchema>;
