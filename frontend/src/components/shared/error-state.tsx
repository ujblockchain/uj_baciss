import { TriangleAlertIcon } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

export const ErrorState = ({
  error,
  onRetry,
}: {
  error: Error;
  onRetry?: () => void;
}) => {
  return (
    <Alert variant="destructive">
      <TriangleAlertIcon />
      <AlertTitle>Something went wrong</AlertTitle>
      <AlertDescription>
        <p>{error.message}</p>
        {onRetry && (
          <Button variant="outline" size="sm" className="mt-2" onClick={onRetry}>
            Try again
          </Button>
        )}
      </AlertDescription>
    </Alert>
  );
};
