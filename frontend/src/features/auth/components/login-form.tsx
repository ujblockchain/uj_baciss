"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { TextField } from "@/components/shared/form-fields";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FieldGroup } from "@/components/ui/field";
import { useAuth } from "@/features/auth/auth-context";
import { loginSchema, type LoginValues } from "@/features/auth/schemas";
import {
  SHOW_TEST_ACCOUNTS,
  TEST_ACCOUNTS,
} from "@/features/auth/test-accounts";
import { ApiError } from "@/lib/api-client";

export const LoginForm = () => {
  const { signIn } = useAuth();
  const form = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = async (values: LoginValues) => {
    try {
      await signIn(values);
    } catch (error) {
      const message =
        error instanceof ApiError ? error.message : "Cannot reach the server.";
      form.setError("root", { message });
    }
  };

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Sign in</CardTitle>
        <CardDescription>Community Voice service-delivery reports</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
          <FieldGroup>
            <TextField
              control={form.control}
              name="email"
              label="Email"
              type="email"
              autoComplete="username"
            />
            <TextField
              control={form.control}
              name="password"
              label="Password"
              type="password"
              autoComplete="current-password"
            />
            {form.formState.errors.root && (
              <Alert variant="destructive">
                <AlertDescription>{form.formState.errors.root.message}</AlertDescription>
              </Alert>
            )}
            <Button type="submit" disabled={form.formState.isSubmitting}>
              {form.formState.isSubmitting ? "Signing in…" : "Sign in"}
            </Button>
          </FieldGroup>
        </form>
        {SHOW_TEST_ACCOUNTS && (
          <div className="mt-6 space-y-2 border-t pt-4">
            <p className="text-xs text-muted-foreground">
              Demo accounts (development only)
            </p>
            <div className="flex flex-wrap gap-2">
              {TEST_ACCOUNTS.map(({ label, email, password }) => (
                <Button
                  key={email}
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => form.reset({ email, password })}
                >
                  {label}
                </Button>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
