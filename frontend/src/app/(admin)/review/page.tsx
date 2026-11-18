import type { Metadata } from "next";

import { ReviewScreen } from "@/features/review/components/review-screen";

export const metadata: Metadata = { title: "Review queue" };

const ReviewPage = () => {
  return <ReviewScreen />;
};

export default ReviewPage;
