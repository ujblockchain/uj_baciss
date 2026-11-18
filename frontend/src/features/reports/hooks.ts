import { useMutation, useQuery } from "@tanstack/react-query";

import {
  fetchMyReports,
  fetchSamples,
  transcribeAudio,
  uploadPhoto,
} from "@/features/reports/api";
import { queryKeys } from "@/lib/query-keys";

export const useSamples = () =>
  useQuery({ queryKey: queryKeys.samples, queryFn: fetchSamples, staleTime: Infinity });

/** The signed-in citizen's reports. Refreshes so a status change appears by itself. */
export const useMyReports = () =>
  useQuery({
    queryKey: queryKeys.myReports,
    queryFn: fetchMyReports,
    refetchInterval: 15_000,
  });

export const useTranscribe = () => useMutation({ mutationFn: transcribeAudio });

export const useAttachPhoto = () =>
  useMutation({
    mutationFn: ({ reportId, file }: { reportId: string; file: File }) =>
      uploadPhoto(reportId, file),
  });
