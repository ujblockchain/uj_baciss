"use client";

import type { ReactNode } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { NAV_ITEMS } from "@/config/navigation";
import { useAuth } from "@/features/auth/auth-context";
import { cn } from "@/lib/utils";

/** The header and page frame for signed-in screens. */
export const AppShell = ({ children }: { children: ReactNode }) => {
  const auth = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  if (auth.status !== "signed-in") return null;
  const { user } = auth;

  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b bg-card">
        <div className="mx-auto flex h-14 max-w-6xl items-center gap-6 px-4">
          <span className="font-semibold tracking-tight">Community Voice</span>
          <nav className="flex flex-1 items-center gap-1" aria-label="Main">
            {NAV_ITEMS[user.role].map((item) => (
              <Link
                key={item.href}
                href={item.href}
                aria-current={pathname === item.href ? "page" : undefined}
                className={cn(
                  "rounded-md px-3 py-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground",
                  pathname === item.href && "bg-muted font-medium text-foreground",
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden sm:inline">{user.name}</span>
            <Badge variant="secondary">{user.role}</Badge>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                auth.signOut();
                router.replace("/login");
              }}
            >
              Sign out
            </Button>
          </div>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl flex-1 space-y-6 p-4 py-6">
        {children}
      </main>
    </div>
  );
};
