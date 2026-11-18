import type { ReactNode } from "react";

import { RoleLayout } from "@/components/layout/role-layout";

const CitizenLayout = ({ children }: { children: ReactNode }) => {
  return <RoleLayout role="citizen">{children}</RoleLayout>;
};

export default CitizenLayout;
