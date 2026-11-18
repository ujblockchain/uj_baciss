import { Skeleton } from "@/components/ui/skeleton";

export const LoadingState = ({ rows = 3 }: { rows?: number }) => {
  return (
    <div className="space-y-3" role="status" aria-label="Loading">
      {Array.from({ length: rows }, (_, i) => (
        <Skeleton key={i} className="h-16 w-full" />
      ))}
    </div>
  );
};

export const PageSkeleton = () => {
  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 p-6">
      <Skeleton className="h-8 w-56" />
      <LoadingState />
    </div>
  );
};
