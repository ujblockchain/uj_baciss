/**
 * The login token, kept in sessionStorage (cleared when the tab closes).
 * It is an external store so React can subscribe to changes.
 * Production note: prefer an httpOnly cookie; a script-injection bug can read this.
 */
const KEY = "community-voice.token";
const listeners = new Set<() => void>();

const notify = () => {
  listeners.forEach((listener) => listener());
};

export const tokenStore = {
  get: (): string | null =>
    typeof window === "undefined" ? null : sessionStorage.getItem(KEY),
  set: (token: string) => {
    sessionStorage.setItem(KEY, token);
    notify();
  },
  clear: () => {
    sessionStorage.removeItem(KEY);
    notify();
  },
  subscribe: (listener: () => void) => {
    listeners.add(listener);
    return () => {
      listeners.delete(listener);
    };
  },
};
