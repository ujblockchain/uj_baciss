import { z } from "zod";

import { categorySchema, urgencySchema } from "@/schemas/domain";
import { reportRecordSchema } from "@/schemas/report";

export const triageSchema = z.object({
  language: z.string(),
  english_text: z.string(),
  category: categorySchema,
  summary: z.string(),
  urgency: urgencySchema,
  urgency_reason: z.string(),
  area_mentioned: z.string().nullable(),
});

export const routingSchema = z.object({
  municipality: z.string(),
  department: z.string(),
  needs_human: z.boolean(),
  reason: z.string(),
});

export const contextSchema = z.object({
  finding: z.string(),
  summary: z.string(),
  confidence: z.string(),
  sources: z.array(z.object({ title: z.string(), url: z.string() })),
});

export const duplicateSchema = z.object({
  duplicate_of: z.string().nullable(),
  reason: z.string(),
});

/** What the reviewer sees while a report waits for the first decision. */
export const reviewPayloadSchema = z.object({
  text: z.string(),
  triage: triageSchema,
  routing: routingSchema,
  context: contextSchema.nullable(),
  duplicate: duplicateSchema,
});

/** What the reviewer sees while the drafted reply waits for approval. */
export const draftPayloadSchema = z.object({
  department: z.string(),
  draft: z.object({ body: z.string(), policy_sources: z.array(z.string()) }),
});

const detailBase = { report: reportRecordSchema, has_photo: z.boolean() };

export const reportDetailSchema = z.union([
  z.object({
    ...detailBase,
    waiting_for: z.literal("review"),
    pending: reviewPayloadSchema,
  }),
  z.object({
    ...detailBase,
    waiting_for: z.literal("draft"),
    pending: draftPayloadSchema,
  }),
  z.object({ ...detailBase, waiting_for: z.null() }),
]);

export const draftOutcomeSchema = z.object({ report_id: z.string(), status: z.string() });

/** The review form. Corrections start as the AI's answer and are sent only if changed. */
export const decisionSchema = z.object({
  category: categorySchema,
  urgency: urgencySchema,
  department: z.string().trim().min(1, "Enter a department."),
  note: z.string().max(500, "Keep the note under 500 characters."),
});

export type ReviewPayload = z.infer<typeof reviewPayloadSchema>;
export type DraftPayload = z.infer<typeof draftPayloadSchema>;
export type ReportDetail = z.infer<typeof reportDetailSchema>;
export type DecisionValues = z.infer<typeof decisionSchema>;
