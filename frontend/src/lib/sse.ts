import { EventSourceParserStream } from "eventsource-parser/stream";

import { apiRequest, jsonBody } from "@/lib/api-client";

export type SseMessage = { event: string; data: unknown };

/**
 * POST and yield each server-sent event as it arrives.
 * The browser's EventSource cannot POST or send a token, so we read the
 * stream ourselves. There is no automatic reconnect: a POST must never repeat.
 */
export async function* streamEvents(
  path: string,
  body: unknown,
  signal?: AbortSignal,
): AsyncGenerator<SseMessage> {
  const response = await apiRequest(path, { ...jsonBody(body), signal });
  if (!response.body) throw new Error("The server sent no stream.");

  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .pipeThrough(new EventSourceParserStream())
    .getReader();
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) return;
      yield { event: value.event ?? "message", data: JSON.parse(value.data) };
    }
  } finally {
    reader.releaseLock();
  }
}
