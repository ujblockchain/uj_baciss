"use client";

import type { ReactNode } from "react";
import {
  environmentManager,
  QueryClient,
  QueryClientProvider,
} from "@tanstack/react-query";

import { Toaster } from "@/components/ui/sonner";
import { AuthProvider } from "@/features/auth/auth-context";
import { TraceProvider } from "@/features/runs/trace-context";
import { ApiError } from "@/lib/api-client";

const makeQueryClient = () => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        // A wrong request will not fix itself: retry only server and network trouble.
        retry: (count, error) =>
          count < 2 && !(error instanceof ApiError && error.status < 500),
      },
    },
  });
};

let browserQueryClient: QueryClient | undefined;

/** A new client per server request; one shared client in the browser. */
const getQueryClient = () => {
  if (environmentManager.isServer()) return makeQueryClient();
  browserQueryClient ??= makeQueryClient();
  return browserQueryClient;
};

export const Providers = ({ children }: { children: ReactNode }) => {
  return (
    <QueryClientProvider client={getQueryClient()}>
      <AuthProvider>
        <TraceProvider>
          {children}
          <Toaster richColors position="top-right" />
        </TraceProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
};
