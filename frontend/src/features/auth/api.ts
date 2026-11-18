import { apiJson, formBody } from "@/lib/api-client";

import {
  tokenSchema,
  userSchema,
  type LoginValues,
} from "@/features/auth/schemas";

/** The API's login takes a form, with the email in the "username" field. */
export const login = async ({ email, password }: LoginValues): Promise<string> => {
  const { access_token } = await apiJson(
    "/auth/login",
    tokenSchema,
    formBody({ username: email, password }),
  );
  return access_token;
};

export const fetchMe = () => apiJson("/me", userSchema);
