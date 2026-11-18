/**
 * The public demo accounts from the README. Shown only in development.
 * 
 */
export const TEST_ACCOUNTS = [
  { label: "Admin", email: "admin@communityvoice.test", password: "AdminPass123" },
  { label: "Citizen 1", email: "citizen1@communityvoice.test", password: "Citizen1Pass123" },
  { label: "Citizen 2", email: "citizen2@communityvoice.test", password: "Citizen2Pass123" },
] as const;

export const SHOW_TEST_ACCOUNTS = process.env.NODE_ENV !== "production";
