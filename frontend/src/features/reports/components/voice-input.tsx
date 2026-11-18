import { useCallback, useRef } from "react";
import { MicIcon, SquareIcon, UploadIcon } from "lucide-react";
import { toast } from "sonner";

import { WarningAlert } from "@/components/shared/warning-alert";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import { MAX_AUDIO_BYTES, AUDIO_ACCEPT } from "@/features/reports/constants";
import { useTranscribe } from "@/features/reports/hooks";
import { useVoiceRecorder } from "@/features/reports/use-voice-recorder";

type Props = { onTranscript: (text: string) => void };

/** Record or upload a voice note and turn it into text the citizen can check. */
export const VoiceInput = ({ onTranscript }: Props) => {
  const transcribe = useTranscribe();
  const fileInput = useRef<HTMLInputElement>(null);
  const { mutate } = transcribe;

  const handleFile = useCallback(
    (file: File) => {
      if (file.size > MAX_AUDIO_BYTES) {
        toast.error("The recording is too large (limit 10 MB).");
        return;
      }
      mutate(file, {
        onSuccess: (result) => onTranscript(result.text),
        onError: (error) => toast.error(error.message),
      });
    },
    [mutate, onTranscript],
  );

  const recorder = useVoiceRecorder(handleFile);

  return (
    <Field>
      <FieldLabel>Voice note (optional)</FieldLabel>
      <div className="flex flex-wrap gap-2">
        {recorder.recording ? (
          <Button type="button" variant="destructive" onClick={recorder.stop}>
            <SquareIcon data-icon="inline-start" /> Stop recording
          </Button>
        ) : (
          <Button type="button" variant="outline" onClick={recorder.start}>
            <MicIcon data-icon="inline-start" /> Record
          </Button>
        )}
        <Button
          type="button"
          variant="outline"
          onClick={() => fileInput.current?.click()}
        >
          <UploadIcon data-icon="inline-start" /> Upload a recording
        </Button>
        <input
          ref={fileInput}
          type="file"
          accept={AUDIO_ACCEPT}
          className="sr-only"
          tabIndex={-1}
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (file) handleFile(file);
            event.target.value = "";
          }}
        />
      </div>
      <FieldDescription>
        {transcribe.isPending
          ? "Transcribing…"
          : "The text appears below. Please check and correct it before you submit."}
      </FieldDescription>
      {recorder.error && (
        <Alert variant="destructive">
          <AlertDescription>{recorder.error}</AlertDescription>
        </Alert>
      )}
      {transcribe.data && (
        <WarningAlert title="Check the text">{transcribe.data.warning}</WarningAlert>
      )}
    </Field>
  );
};
