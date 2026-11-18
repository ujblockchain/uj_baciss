import type { ReactNode } from "react";

import { RoleLayout } from "@/components/layout/role-layout";

const AdminLayout = ({ children }: { children: ReactNode }) => {
  return <RoleLayout role="admin">{children}</RoleLayout>;
};

export default AdminLayout;
