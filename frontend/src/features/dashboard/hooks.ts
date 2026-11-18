import { useQuery } from "@tanstack/react-query";

import { fetchStats } from "@/features/dashboard/api";
import { queryKeys } from "@/lib/query-keys";

export const useStats = () =>
  useQuery({ queryKey: queryKeys.stats, queryFn: fetchStats, refetchInterval: 30_000 });
