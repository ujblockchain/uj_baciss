"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/features/auth/auth-context";
import { PageSkeleton } from "@/components/shared/loading-state";
import { HOME_PATH } from "@/config/navigation";

/**
 * Sends a signed-in user to their home screen.
 * With `fallback` it also works as a page: signed-out users see the fallback.
 */
export const SignedInRedirect = ({
  fallback,
}: {
  fallback?: React.ReactNode;
}) => {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (auth.status === "signed-in") router.replace(HOME_PATH[auth.user.role]);
    else if (auth.status === "signed-out" && !fallback) router.replace("/login");
  }, [auth, fallback, router]);

  if (auth.status === "signed-out" && fallback) return fallback;
  return <PageSkeleton />;
};
