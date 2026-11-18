import { z } from "zod";

import { apiJson, jsonBody } from "@/lib/api-client";
import { draftOutcomeSchema, reportDetailSchema } from "@/features/review/schemas";
import { reportRecordSchema } from "@/schemas/report";

export const fetchQueue = () => apiJson("/reviews", z.array(reportRecordSchema));

export const fetchReportDetail = (id: string) =>
  apiJson(`/reports/${id}`, reportDetailSchema);

export type DraftDecision = { action: "approve" | "reject"; text?: string };

export const sendDraftDecision = (id: string, decision: DraftDecision) =>
  apiJson(`/reports/${id}/draft`, draftOutcomeSchema, jsonBody(decision));
