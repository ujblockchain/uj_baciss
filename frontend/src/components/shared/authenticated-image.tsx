import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { Skeleton } from "@/components/ui/skeleton";
import { apiBlob } from "@/lib/api-client";
import { queryKeys } from "@/lib/query-keys";

/**
 * An image that needs the login token. A plain <img> cannot send the
 * Authorization header, so we fetch the bytes and show them from memory.
 */
export const AuthenticatedImage = ({ path, alt }: { path: string; alt: string }) => {
  const { data, isPending, isError } = useQuery({
    queryKey: queryKeys.photo(path),
    queryFn: () => apiBlob(path),
    staleTime: Infinity,
  });
  const url = useMemo(() => (data ? URL.createObjectURL(data) : null), [data]);

  useEffect(() => {
    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [url]);

  if (isPending) return <Skeleton className="h-40 w-56" />;
  if (isError || !url) return null;
  return (
    // eslint-disable-next-line @next/next/no-img-element -- an in-memory blob, not optimisable
    <img src={url} alt={alt} className="max-h-72 rounded-lg border object-contain" />
  );
};
