import { apiJson } from "@/lib/api-client";
import { statsSchema } from "@/features/dashboard/schemas";

export const fetchStats = () => apiJson("/stats", statsSchema);
