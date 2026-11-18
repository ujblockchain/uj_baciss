import { z } from "zod";

export const roleSchema = z.enum(["citizen", "admin"]);

export const userSchema = z.object({
  id: z.number(),
  email: z.string(),
  name: z.string(),
  role: roleSchema,
});

export const tokenSchema = z.object({ access_token: z.string() });

export const loginSchema = z.object({
  email: z.email("Enter a valid email address."),
  password: z.string().min(1, "Enter your password."),
});

export type Role = z.infer<typeof roleSchema>;
export type User = z.infer<typeof userSchema>;
export type LoginValues = z.infer<typeof loginSchema>;
