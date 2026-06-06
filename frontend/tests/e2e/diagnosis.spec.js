import { test, expect } from "@playwright/test";

test("deve concluir o fluxo principal de diagnóstico", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", {
    name: /testar diagnóstico/i,
  }).click();

  await expect(page).toHaveURL(/collection/);

  await page.getByLabel(/receita mensal/i).fill("2500");

  await page.getByLabel(/despesas mensais/i).fill("980");

  await page.getByLabel(/dívida atual/i).fill("250");

  await page.getByLabel(/reserva financeira/i).fill("760");

  await page.getByRole("button", {
    name: /calcular meu diagnóstico/i,
  }).click();

  await expect(page).toHaveURL(/result/);
});