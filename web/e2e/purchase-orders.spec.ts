import { test, expect } from '@playwright/test';

// All tests in this file require the user to be logged in.
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  // Check if already on dashboard, if not, login.
  const dashboardHeading = page.getByRole('heading', { name: 'Dashboard' });
  if (!await dashboardHeading.isVisible()) {
    await page.getByLabel('Email').fill('admin@example.com');
    await page.getByLabel('Password').fill('admin');
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForURL('/');
  }
});

test('should allow a manager to create a new purchase order', async ({ page }) => {
  // Pre-requisite: Ensure at least one supplier and one item exist.
  // For a robust test suite, this would be handled by API fixtures.
  // For now, we assume the seed data provides this.

  // Navigate to the Purchase Orders page
  await page.getByRole('link', { name: 'Purchase Orders' }).click();
  await page.waitForURL('**/purchase-orders');

  // Click the "Create Purchase Order" button
  await page.getByRole('button', { name: 'Create Purchase Order' }).click();

  // The form modal or page should appear
  await expect(page.getByRole('heading', { name: 'Create Purchase Order' })).toBeVisible();

  // Select a supplier
  // This assumes a combobox/select with a label. The exact locator might differ.
  await page.getByLabel('Supplier').click();
  // We assume a supplier named 'Test Supplier' exists from seed data
  await page.getByRole('option', { name: 'Test Supplier' }).first().click();

  // Add a line item
  await page.getByRole('button', { name: 'Add Item' }).click();

  // Fill in the first line item row
  const firstRow = page.getByRole('row').last();

  // Select an item. This assumes an autocomplete/combobox.
  // We assume an item named 'Carrots' exists.
  await firstRow.getByLabel('Item').fill('Carrots');
  await page.getByRole('option', { name: 'Carrots' }).first().click();

  // Enter quantity
  await firstRow.getByLabel('Quantity Ordered').fill('50');

  // Submit the form
  await page.getByRole('button', { name: 'Save' }).click();

  // The new PO should now be in the table.
  // We'll check for the supplier name to confirm creation.
  await expect(page.getByRole('cell', { name: 'Test Supplier' })).toBeVisible();
  // We can also check for the status
  await expect(page.getByRole('cell', { name: 'DRAFT' })).toBeVisible();
});
