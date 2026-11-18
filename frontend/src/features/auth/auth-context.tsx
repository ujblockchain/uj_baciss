import {
  createContext,
  useContext,
  useMemo,
  useSyncExternalStore,
  type ReactNode,
} from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { fetchMe, login } from "@/features/auth/api";
import type { LoginValues, User } from "@/features/auth/schemas";
import { queryKeys } from "@/lib/query-keys";
import { tokenStore } from "@/lib/token-store";

type AuthState =
  | { status: "loading" }
  | { status: "signed-out" }
  | { status: "signed-in"; user: User };

type AuthContextValue = AuthState & {
  signIn: (values: LoginValues) => Promise<void>;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const queryClient = useQueryClient();
  // undefined on the server and during hydration: we do not know yet.
  const token = useSyncExternalStore(
    tokenStore.subscribe,
    tokenStore.get,
    () => undefined,
  );
  const me = useQuery({
    queryKey: queryKeys.me,
    queryFn: fetchMe,
    enabled: Boolean(token),
    retry: false,
  });

  const value = useMemo<AuthContextValue>(() => {
    let state: AuthState = { status: "loading" };
    if (token === null || me.isError) state = { status: "signed-out" };
    else if (token && me.data) state = { status: "signed-in", user: me.data };

    return {
      ...state,
      signIn: async (values) => {
        queryClient.clear();
        tokenStore.set(await login(values));
      },
      signOut: () => {
        tokenStore.clear();
        queryClient.clear();
      },
    };
  }, [token, me.data, me.isError, queryClient]);

  return <AuthContext value={value}>{children}</AuthContext>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside <AuthProvider>.");
  return context;
};
