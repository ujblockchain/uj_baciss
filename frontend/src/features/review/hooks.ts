import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  fetchQueue,
  fetchReportDetail,
  sendDraftDecision,
  type DraftDecision,
} from "@/features/review/api";
import { queryKeys } from "@/lib/query-keys";

export const useReviewQueue = () =>
  useQuery({
    queryKey: queryKeys.queue,
    queryFn: fetchQueue,
    refetchInterval: 15_000,
  });

export const useReportDetail = (id: string) =>
  useQuery({
    queryKey: queryKeys.report(id),
    queryFn: () => fetchReportDetail(id),
  });

export const useDraftDecision = (id: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (decision: DraftDecision) => sendDraftDecision(id, decision),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.review }),
  });
};
