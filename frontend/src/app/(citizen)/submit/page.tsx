import type { Metadata } from "next";

import { SubmitScreen } from "@/features/reports/components/submit-screen";

export const metadata: Metadata = { title: "Submit a report" };

const SubmitPage = () => {
  return <SubmitScreen />;
};

export default SubmitPage;
