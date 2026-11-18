import type { Metadata } from "next";

import { DashboardScreen } from "@/features/dashboard/components/dashboard-screen";

export const metadata: Metadata = { title: "Dashboard" };

const DashboardPage = () => {
  return <DashboardScreen />;
};

export default DashboardPage;
