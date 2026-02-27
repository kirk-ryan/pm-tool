import { expect, test, type Page } from "@playwright/test";

async function loginAsUser(page: Page) {
  await page.goto("/login");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: /sign in/i }).click();
  await page.waitForURL("/");
}

test("redirects unauthenticated user to login page", async ({ page }) => {
  await page.goto("/");
  await page.waitForURL(/\/login/);
  await expect(page.getByLabel("Username")).toBeVisible();
  await expect(page.getByLabel("Password")).toBeVisible();
});

test("shows error on incorrect credentials", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Username").fill("admin");
  await page.getByLabel("Password").fill("wrongpassword");
  await page.getByRole("button", { name: /sign in/i }).click();
  await expect(page.getByRole("alert").filter({ hasText: /invalid/i })).toBeVisible();
});

test("stays on login page with wrong password for valid username", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("wrong");
  await page.getByRole("button", { name: /sign in/i }).click();
  await expect(page.getByRole("alert").filter({ hasText: /invalid/i })).toBeVisible();
  await expect(page).toHaveURL(/\/login/);
});

test("login with correct credentials shows the board", async ({ page }) => {
  await loginAsUser(page);
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
  await expect(page.locator('[data-testid^="column-"]')).toHaveCount(5);
});

test("logout redirects back to login", async ({ page }) => {
  await loginAsUser(page);
  await page.getByRole("button", { name: /sign out/i }).click();
  await page.waitForURL(/\/login/);
  await expect(page.getByLabel("Username")).toBeVisible();
});

test("authenticated user visiting /login is redirected to board", async ({ page }) => {
  await loginAsUser(page);
  await page.goto("/login");
  await page.waitForURL("/");
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
});
