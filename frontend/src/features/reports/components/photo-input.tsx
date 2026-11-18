import { Button } from "@/components/ui/button";
import { Field, FieldDescription, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { MAX_PHOTO_BYTES, PHOTO_ACCEPT } from "@/features/reports/constants";
import { useState } from "react";

type Props = { file: File | null; onChange: (file: File | null) => void };

/** An optional photo for the reviewer, checked for size before upload. */
export const PhotoInput = ({ file, onChange }: Props) => {
  const [error, setError] = useState<string | null>(null);

  return (
    <Field data-invalid={Boolean(error)}>
      <FieldLabel htmlFor="photo">Photo (optional)</FieldLabel>
      {file ? (
        <div className="flex items-center gap-3 text-sm">
          <span className="truncate">{file.name}</span>
          <Button type="button" variant="ghost" size="sm" onClick={() => onChange(null)}>
            Remove
          </Button>
        </div>
      ) : (
        <Input
          id="photo"
          type="file"
          accept={PHOTO_ACCEPT}
          onChange={(event) => {
            const chosen = event.target.files?.[0] ?? null;
            if (chosen && chosen.size > MAX_PHOTO_BYTES) {
              setError("The photo is too large (limit 5 MB).");
              onChange(null);
              return;
            }
            setError(null);
            onChange(chosen);
          }}
        />
      )}
      <FieldDescription>Only the reviewer sees it. JPEG, PNG or WebP, up to 5 MB.</FieldDescription>
      {error && <FieldError>{error}</FieldError>}
    </Field>
  );
};
