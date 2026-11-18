import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useSamples } from "@/features/reports/hooks";

/** Demo helper: fills the report box with one of the sample reports. */
export const SamplePicker = ({ onPick }: { onPick: (text: string) => void }) => {
  const { data: samples } = useSamples();
  if (!samples) return null;

  const labels = Object.fromEntries(
    samples.map((s) => [s.id, `${s.language}: ${s.text.slice(0, 60)}`]),
  );

  return (
    <Field>
      <FieldLabel htmlFor="sample">Sample report (demo)</FieldLabel>
      <Select
        items={labels}
        onValueChange={(id) => {
          const sample = samples.find((s) => s.id === id);
          if (sample) onPick(sample.text);
        }}
      >
        <SelectTrigger id="sample" className="w-full">
          <SelectValue placeholder="Choose a sample" />
        </SelectTrigger>
        <SelectContent>
          {samples.map((sample) => (
            <SelectItem key={sample.id} value={sample.id}>
              {labels[sample.id]}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <FieldDescription>Fictional reports in several languages.</FieldDescription>
    </Field>
  );
};
