import type { Role } from "@/features/auth/schemas";

export type NavItem = { href: string; label: string };

export const NAV_ITEMS: Record<Role, NavItem[]> = {
  citizen: [
    { href: "/submit", label: "Submit a report" },
    { href: "/my-reports", label: "My reports" },
  ],
  admin: [
    { href: "/review", label: "Review queue" },
    { href: "/dashboard", label: "Dashboard" },
  ],
};

/** Where each role lands after signing in. */
export const HOME_PATH: Record<Role, string> = {
  citizen: "/submit",
  admin: "/review",
};
