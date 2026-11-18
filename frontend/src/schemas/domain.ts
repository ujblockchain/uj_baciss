import { z } from "zod";

export const CATEGORIES = [
  "water",
  "electricity",
  "roads",
  "sanitation",
  "waste",
  "other",
] as const;
export const URGENCIES = ["low", "medium", "high", "critical"] as const;

export const categorySchema = z.enum(CATEGORIES);
export const urgencySchema = z.enum(URGENCIES);

export type Category = z.infer<typeof categorySchema>;
export type Urgency = z.infer<typeof urgencySchema>;
