import { useCallback, useRef, useState } from "react";

/** A file extension the API accepts, for what the browser recorded. */
const extensionFor = (mimeType: string): string => {
  if (mimeType.includes("webm")) return "webm";
  if (mimeType.includes("ogg")) return "ogg";
  if (mimeType.includes("mp4") || mimeType.includes("aac")) return "m4a";
  return "wav";
};

/** Records from the microphone and hands back the finished recording as a file. */
export const useVoiceRecorder = (onRecorded: (file: File) => void) => {
  const [recording, setRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const recorder = useRef<MediaRecorder | null>(null);

  const start = useCallback(async () => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const media = new MediaRecorder(stream);
      const chunks: Blob[] = [];
      media.ondataavailable = (event) => chunks.push(event.data);
      media.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        const type = media.mimeType || "audio/webm";
        onRecorded(new File(chunks, `voice.${extensionFor(type)}`, { type }));
        setRecording(false);
      };
      media.start();
      recorder.current = media;
      setRecording(true);
    } catch {
      setError("The microphone is not available. Allow access, or upload a recording.");
    }
  }, [onRecorded]);

  const stop = useCallback(() => recorder.current?.stop(), []);

  return { recording, error, start, stop };
};
