import type { Metadata } from "next";

import { MyReportsScreen } from "@/features/reports/components/my-reports-screen";

export const metadata: Metadata = { title: "My reports" };

const MyReportsPage = () => {
  return <MyReportsScreen />;
};

export default MyReportsPage;
