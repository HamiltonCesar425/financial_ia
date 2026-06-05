import { defineConfig } from "@playwright/test";
import process from "node:process";

export default defineConfig({
    testDir: "./tests/e2e",

    retries: process.env.CI ? 2 : 0,

    timeout: 30_000,
    use: {
        baseURL: "http://localhost:5173",
        headless: true,
    },
    webServer: {
        command: "npm run dev -- --host 0.0.0.0",
        port: 5173,
        reuseExistingServer: true,
        timeout: 120_000,
    },
});