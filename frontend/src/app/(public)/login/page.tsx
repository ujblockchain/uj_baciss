import type { Metadata } from "next";

import { LoginForm } from "@/features/auth/components/login-form";
import { SignedInRedirect } from "@/features/auth/components/signed-in-redirect";

export const metadata: Metadata = { title: "Sign in" };

const LoginPage = () => {
  return (
    <SignedInRedirect
      fallback={
        <div className="flex min-h-screen items-center justify-center p-4">
          <LoginForm />
        </div>
      }
    />
  );
};

export default LoginPage;
