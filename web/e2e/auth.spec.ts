import { test, expect } from '@playwright/test';

test('should allow a user to log in and see the dashboard', async ({ page }) => {
  // Start from the home page, which should redirect to login
  await page.goto('/');

  // The page should be on the login screen
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();

  // Fill in the credentials
  await page.getByLabel('Email').fill('admin@example.com');
  await page.getByLabel('Password').fill('admin');

  // Click the login button
  await page.getByRole('button', { name: 'Login' }).click();

  // After login, the user should be redirected to the dashboard
  await page.waitForURL('**/dashboard**'); // Note: In this app, dashboard is the root '/'
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // Check for a key metric on the dashboard to confirm it loaded
  await expect(page.getByText('Total Inventory Value')).toBeVisible();
});
