import type { z } from "zod";

import { API_URL } from "@/lib/config";
import { tokenStore } from "@/lib/token-store";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type RequestOptions = Omit<RequestInit, "headers"> & {
  headers?: Record<string, string>;
};

const errorMessage = async (response: Response): Promise<string> => {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
  } catch {
    // The body was not JSON; fall through.
  }
  return `The request failed (${response.status}).`;
};

/** Send a request with the signed-in token. Throws ApiError unless it succeeds. */
export const apiRequest = async (
  path: string,
  { headers, ...init }: RequestOptions = {},
): Promise<Response> => {
  const token = tokenStore.get();
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { ...(token && { Authorization: `Bearer ${token}` }), ...headers },
  });
  if (!response.ok) {
    if (response.status === 401) tokenStore.clear(); // the session ended
    throw new ApiError(response.status, await errorMessage(response));
  }
  return response;
};

/** Request JSON and check its shape, so a changed API fails loudly here. */
export const apiJson = async <S extends z.ZodType>(
  path: string,
  schema: S,
  options?: RequestOptions,
): Promise<z.output<S>> => {
  const response = await apiRequest(path, options);
  return schema.parse(await response.json());
};

export const apiBlob = async (path: string): Promise<Blob> => {
  return (await apiRequest(path)).blob();
};

export const jsonBody = (data: unknown, method = "POST"): RequestOptions => {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };
};

/** A file upload. The browser adds the multipart header itself. */
export const fileBody = (method: string, field: string, file: File): RequestOptions => {
  const body = new FormData();
  body.append(field, file, file.name);
  return { method, body };
};

export const formBody = (data: Record<string, string>): RequestOptions => {
  return {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(data),
  };
};
