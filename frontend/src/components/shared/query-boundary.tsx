import type { ReactNode } from "react";
import type { UseQueryResult } from "@tanstack/react-query";

import { EmptyState } from "@/components/shared/empty-state";
import { ErrorState } from "@/components/shared/error-state";
import { LoadingState } from "@/components/shared/loading-state";

/** Handles loading, error and empty for a query, so screens only draw the data. */
export const QueryBoundary = <T,>({
  query,
  emptyMessage,
  isEmpty,
  children,
}: {
  query: UseQueryResult<T>;
  emptyMessage?: string;
  isEmpty?: (data: T) => boolean;
  children: (data: T) => ReactNode;
}) => {
  if (query.isPending) return <LoadingState />;
  if (query.isError) {
    return <ErrorState error={query.error} onRetry={() => query.refetch()} />;
  }
  if (isEmpty?.(query.data)) return <EmptyState message={emptyMessage ?? "Nothing here yet."} />;
  return <>{children(query.data)}</>;
};
