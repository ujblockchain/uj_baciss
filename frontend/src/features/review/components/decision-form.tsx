import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import {
  SelectField,
  TextField,
  TextareaField,
} from "@/components/shared/form-fields";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FieldGroup } from "@/components/ui/field";
import {
  decisionSchema,
  type DecisionValues,
  type ReviewPayload,
} from "@/features/review/schemas";
import { humanize } from "@/lib/format";
import { CATEGORIES, URGENCIES } from "@/schemas/domain";

const toOptions = (values: readonly string[]) =>
  values.map((value) => ({ value, label: humanize(value) }));

type Props = {
  payload: ReviewPayload;
  disabled: boolean;
  onDecide: (body: Record<string, string>) => void;
};

/** Approve or reject, with optional corrections to what the agents decided. */
export const DecisionForm = ({ payload, disabled, onDecide }: Props) => {
  const { triage, routing } = payload;
  const initial: DecisionValues = {
    category: triage.category,
    urgency: triage.urgency,
    department: routing.department,
    note: "",
  };
  const form = useForm<DecisionValues>({
    resolver: zodResolver(decisionSchema),
    defaultValues: initial,
  });

  const decide = (action: "approve" | "reject") =>
    form.handleSubmit((values) => {
      // Send only what the reviewer changed.
      const corrections = (["category", "urgency", "department"] as const)
        .filter((key) => values[key] !== initial[key])
        .map((key) => [key, values[key]]);
      onDecide({ action, note: values.note, ...Object.fromEntries(corrections) });
    });

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your decision</CardTitle>
      </CardHeader>
      <CardContent>
        <form noValidate>
          <FieldGroup>
            <SelectField
              control={form.control}
              name="category"
              label="Category"
              options={toOptions(CATEGORIES)}
            />
            <SelectField
              control={form.control}
              name="urgency"
              label="Urgency"
              options={toOptions(URGENCIES)}
            />
            <TextField control={form.control} name="department" label="Department" />
            <TextareaField
              control={form.control}
              name="note"
              label="Note (optional)"
              description="Corrections you make are remembered for similar reports."
              rows={3}
            />
            <div className="flex gap-2">
              <Button type="button" disabled={disabled} onClick={decide("approve")}>
                Approve
              </Button>
              <Button
                type="button"
                variant="outline"
                disabled={disabled}
                onClick={decide("reject")}
              >
                Reject
              </Button>
            </div>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
};
