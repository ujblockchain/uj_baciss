/** One place for cache keys, so queries and invalidation always agree. */
export const queryKeys = {
  me: ["me"] as const,
  samples: ["samples"] as const,
  myReports: ["my-reports"] as const,
  review: ["review"] as const, // everything below is invalidated together
  queue: ["review", "queue"] as const,
  report: (id: string) => ["review", "report", id] as const,
  stats: ["review", "stats"] as const,
  photo: (path: string) => ["photo", path] as const,
};
