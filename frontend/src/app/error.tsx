"use client";

import { ErrorState } from "@/components/shared/error-state";

const GlobalError = ({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) => {
  return (
    <div className="mx-auto max-w-lg p-6">
      <ErrorState error={error} onRetry={reset} />
    </div>
  );
};

export default GlobalError;
