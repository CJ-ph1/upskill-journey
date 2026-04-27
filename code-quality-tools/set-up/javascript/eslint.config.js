import js from "@eslint/js";
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  prettier, // disables ESLint rules that conflict with Prettier — keep last
  {
    rules: {
      eqeqeq: "error",
      "no-console": "warn",
      "@typescript-eslint/no-unused-vars": "error",
    },
  },
  {
    ignores: ["node_modules", "dist", "build", "coverage"],
  },
];
