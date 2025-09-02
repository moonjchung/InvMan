import { test, expect } from '@playwright/test';

// This test depends on the user being logged in.
// For a real test suite, we would use a global setup file to handle authentication.
// For this MVP, we will log in at the start of the test.
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.getByLabel('Email').fill('admin@example.com');
  await page.getByLabel('Password').fill('admin');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL('/');
});

test('should allow a manager to create a new item', async ({ page }) => {
  // Navigate to the items page
  await page.getByRole('link', { name: 'Items' }).click();
  await page.waitForURL('**/items**');

  // Click the "Add Item" button
  await page.getByRole('button', { name: 'Add Item' }).click();

  // Fill out the form
  const uniqueSku = `E2E-SKU-${Date.now()}`;
  const itemName = `E2E Test Item`;
  await page.getByLabel('SKU').fill(uniqueSku);
  await page.getByLabel('Name').fill(itemName);
  await page.getByLabel('Price').fill('123.45');
  await page.getByLabel('Stock Level').fill('100');

  // Submit the form
  await page.getByRole('button', { name: 'Save' }).click();

  // The new item should now be in the table.
  // We can find it by its unique SKU.
  await expect(page.getByRole('cell', { name: uniqueSku })).toBeVisible();
  await expect(page.getByRole('cell', { name: itemName })).toBeVisible();
});
