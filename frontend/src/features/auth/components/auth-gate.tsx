"use client";

import { useEffect, type ReactNode } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/features/auth/auth-context";
import type { Role } from "@/features/auth/schemas";
import { PageSkeleton } from "@/components/shared/loading-state";
import { HOME_PATH } from "@/config/navigation";

/** Shows its children only to a signed-in user with the given role. */
export const AuthGate = ({ role, children }: { role: Role; children: ReactNode }) => {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (auth.status === "signed-out") router.replace("/login");
    else if (auth.status === "signed-in" && auth.user.role !== role) {
      router.replace(HOME_PATH[auth.user.role]);
    }
  }, [auth, role, router]);

  if (auth.status !== "signed-in" || auth.user.role !== role) {
    return <PageSkeleton />;
  }
  return children;
};
