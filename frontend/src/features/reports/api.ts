import { z } from "zod";

import { apiJson, fileBody } from "@/lib/api-client";
import {
  myReportSchema,
  photoOutcomeSchema,
  sampleSchema,
  transcriptSchema,
} from "@/features/reports/schemas";

export const fetchSamples = () => apiJson("/samples", z.array(sampleSchema));

export const fetchMyReports = () => apiJson("/my/reports", z.array(myReportSchema));

export const transcribeAudio = (file: File) =>
  apiJson("/transcriptions", transcriptSchema, fileBody("POST", "audio", file));

export const uploadPhoto = (reportId: string, file: File) =>
  apiJson(
    `/reports/${reportId}/photo`,
    photoOutcomeSchema,
    fileBody("PUT", "photo", file),
  );
