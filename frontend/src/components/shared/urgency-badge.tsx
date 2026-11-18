import { Badge } from "@/components/ui/badge";
import { humanize } from "@/lib/format";
import type { Urgency } from "@/schemas/domain";

const VARIANT = {
  critical: "destructive",
  high: "default",
  medium: "secondary",
  low: "outline",
} as const;

export const UrgencyBadge = ({ urgency }: { urgency: Urgency }) => {
  return <Badge variant={VARIANT[urgency]}>{humanize(urgency)}</Badge>;
};
