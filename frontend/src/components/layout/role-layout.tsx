import type { ReactNode } from "react";

import { AppShell } from "@/components/layout/app-shell";
import { AuthGate } from "@/features/auth/components/auth-gate";
import type { Role } from "@/features/auth/schemas";

/** The layout for every screen of one role: guard plus page frame. */
export const RoleLayout = ({ role, children }: { role: Role; children: ReactNode }) => {
  return (
    <AuthGate role={role}>
      <AppShell>{children}</AppShell>
    </AuthGate>
  );
};
