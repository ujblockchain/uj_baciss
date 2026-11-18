import { Badge } from "@/components/ui/badge";

/** The colour follows the status; the words come from the API. */
const variantFor = (status: string) => {
  if (status === "ready_to_send") return "default";
  if (status === "rejected") return "outline";
  return "secondary";
};

export const StageBadge = ({ status, stage }: { status: string; stage: string }) => {
  return <Badge variant={variantFor(status)}>{stage}</Badge>;
};
