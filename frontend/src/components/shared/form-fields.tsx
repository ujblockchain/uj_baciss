import type { ComponentProps } from "react";
import {
  Controller,
  type Control,
  type FieldPath,
  type FieldValues,
} from "react-hook-form";

import {
  Field,
  FieldDescription,
  FieldError,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

/*
 * Form fields wired to react-hook-form: label, control, hint and error message
 * in one place, so no form repeats this markup.
 */
type FieldProps<T extends FieldValues> = {
  control: Control<T>;
  name: FieldPath<T>;
  label: string;
  description?: string;
};

export const TextField = <T extends FieldValues>({
  control,
  name,
  label,
  description,
  ...input
}: FieldProps<T> &
  Pick<ComponentProps<"input">, "type" | "placeholder" | "autoComplete">) => {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <Field data-invalid={fieldState.invalid}>
          <FieldLabel htmlFor={name}>{label}</FieldLabel>
          <Input
            {...field}
            {...input}
            id={name}
            value={field.value ?? ""}
            aria-invalid={fieldState.invalid}
          />
          {description && <FieldDescription>{description}</FieldDescription>}
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
};

export const TextareaField = <T extends FieldValues>({
  control,
  name,
  label,
  description,
  ...textarea
}: FieldProps<T> & Pick<ComponentProps<"textarea">, "rows" | "placeholder">) => {
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <Field data-invalid={fieldState.invalid}>
          <FieldLabel htmlFor={name}>{label}</FieldLabel>
          <Textarea
            {...field}
            {...textarea}
            id={name}
            value={field.value ?? ""}
            aria-invalid={fieldState.invalid}
          />
          {description && <FieldDescription>{description}</FieldDescription>}
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
};

export type Option = { value: string; label: string };

export const SelectField = <T extends FieldValues>({
  control,
  name,
  label,
  description,
  options,
}: FieldProps<T> & { options: readonly Option[] }) => {
  const labels = Object.fromEntries(options.map((o) => [o.value, o.label]));
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState }) => (
        <Field data-invalid={fieldState.invalid}>
          <FieldLabel htmlFor={name}>{label}</FieldLabel>
          <Select
            value={field.value}
            items={labels}
            onValueChange={(value) => value !== null && field.onChange(value)}
          >
            <SelectTrigger id={name} className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {options.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {description && <FieldDescription>{description}</FieldDescription>}
          {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
        </Field>
      )}
    />
  );
};
