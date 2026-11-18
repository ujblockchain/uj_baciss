import type { ReactNode } from "react";
import { TriangleAlertIcon } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

/** A clearly visible amber notice, for things the reader must not miss. */
export const WarningAlert = ({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) => {
  return (
    <Alert
      role="alert"
      className="border-amber-500/50 bg-amber-50 text-amber-950 dark:bg-amber-500/10 dark:text-amber-100"
    >
      <TriangleAlertIcon className="text-amber-600 dark:text-amber-400" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription className="text-amber-900 dark:text-amber-200">
        {children}
      </AlertDescription>
    </Alert>
  );
};
