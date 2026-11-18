"use client";

import { useState } from "react";
import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { PageHeader } from "@/components/shared/page-header";
import { TextareaField } from "@/components/shared/form-fields";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { FieldGroup } from "@/components/ui/field";
import { PhotoInput } from "@/features/reports/components/photo-input";
import { SamplePicker } from "@/features/reports/components/sample-picker";
import { VoiceInput } from "@/features/reports/components/voice-input";
import { useAttachPhoto } from "@/features/reports/hooks";
import { submitSchema, type SubmitValues } from "@/features/reports/schemas";
import { RunProgress } from "@/features/runs/components/run-progress";
import { useRunStream } from "@/features/runs/use-run-stream";

export const SubmitScreen = () => {
  const form = useForm<SubmitValues>({
    resolver: zodResolver(submitSchema),
    defaultValues: { text: "" },
  });
  const [photo, setPhoto] = useState<File | null>(null);
  const run = useRunStream();
  const attachPhoto = useAttachPhoto();

  const setText = (text: string) =>
    form.setValue("text", text, { shouldValidate: true, shouldDirty: true });

  const onSubmit = async (values: SubmitValues) => {
    const result = await run.start("/reports", values);
    const accepted = result.status === "paused" || result.status === "done";
    if (!accepted) return;

    if (photo && result.reportId) {
      attachPhoto.mutate(
        { reportId: result.reportId, file: photo },
        { onError: (error) => toast.error(`Photo not saved: ${error.message}`) },
      );
    }
    toast.success("Your report was received.");
    form.reset();
    setPhoto(null);
  };

  const submitted = run.state.status === "paused" || run.state.status === "done";

  return (
    <div className="mx-auto w-full max-w-[30rem] space-y-6">
      <PageHeader
        title="Submit a report"
        description="Tell us about a service problem in your area, in any of our languages."
      />
      <Card>
        <CardContent>
          <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
            <FieldGroup>
              <SamplePicker onPick={setText} />
              <VoiceInput onTranscript={setText} />
              <TextareaField
                control={form.control}
                name="text"
                label="Describe the problem"
                rows={6}
                placeholder="What is wrong, where, and since when?"
              />
              <PhotoInput file={photo} onChange={setPhoto} />
              <Button type="submit" disabled={run.state.status === "running"}>
                {run.state.status === "running" ? "Submitting…" : "Submit report"}
              </Button>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
      <RunProgress run={run.state} />
      {submitted && (
        <Alert>
          <AlertDescription>
            Thank you. You can follow your report in{" "}
            <Link href="/my-reports" className="font-medium underline">
              My reports
            </Link>
            .
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
};
