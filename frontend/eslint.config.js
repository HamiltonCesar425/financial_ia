import js from "@eslint/js"
import pluginReact from "eslint-plugin-react"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"
import { defineConfig } from "eslint/config"
import globals from "globals"
import eslintConfigPrettier from "eslint-config-prettier"

export default defineConfig([
  {
    ignores: ["dist", "node_modules"],
  },

  {
    files: ["**/*.{js,mjs,cjs,jsx}"],

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",

      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },

      globals: globals.browser,
    },

    plugins: {
      react: pluginReact,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },

    rules: {
      ...js.configs.recommended.rules,
      ...pluginReact.configs.flat.recommended.rules,
      ...reactHooks.configs.recommended.rules,

      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
    },

    settings: {
      react: {
        version: "detect",
      },
    },
  },
  eslintConfigPrettier,
])
