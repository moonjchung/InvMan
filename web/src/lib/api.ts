const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  if (!token) {
    return {};
  }
  return {
    'Authorization': `Bearer ${token}`,
  };
}

async function request(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const headers: HeadersInit = {
    ...getAuthHeaders(),
    ...options.headers,
  };

  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    // TODO: better error handling
    console.error('API request failed', response);
    throw new Error('API request failed');
  }

  if (response.status === 204) { // No Content
    return;
  }

  return response.json();
}

// Auth
export const getUsersMe = () => request('/users/me');

// Settings
export const getSettings = () => request('/settings');

// Items
export const getItems = () => request('/items');
export const getItemBySku = (sku: string) => request(`/items/sku/${sku}`);
export const createItem = (data: any) => request('/items', { method: 'POST', body: JSON.stringify(data) });
export const updateItem = (id: number, data: any) => request(`/items/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteItem = (id: number) => request(`/items/${id}`, { method: 'DELETE' });
export const adjustStock = (id: number, data: any) => request(`/items/${id}/adjust`, { method: 'POST', body: JSON.stringify(data) });
export const exportItemsCsv = async () => {
  const url = `${API_BASE_URL}/items/export/csv`;
  const headers = getAuthHeaders();
  const response = await fetch(url, { headers });
  if (!response.ok) {
    throw new Error('Export failed');
  }
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = 'items.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
};
export const importItemsCsv = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return request('/items/import/csv', {
    method: 'POST',
    body: formData,
  });
};

// Categories
export const getCategories = () => request('/categories');
export const createCategory = (data: any) => request('/categories', { method: 'POST', body: JSON.stringify(data) });
export const updateCategory = (id: number, data: any) => request(`/categories/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteCategory = (id: number) => request(`/categories/${id}`, { method: 'DELETE' });

// Suppliers
export const getSuppliers = () => request('/suppliers');
export const createSupplier = (data: any) => request('/suppliers', { method: 'POST', body: JSON.stringify(data) });
export const updateSupplier = (id: number, data: any) => request(`/suppliers/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteSupplier = (id: number) => request(`/suppliers/${id}`, { method: 'DELETE' });

// Purchase Orders
export const getPurchaseOrders = () => request('/purchase-orders');
export const getPurchaseOrder = (id: number) => request(`/purchase-orders/${id}`);
export const createPurchaseOrder = (data: any) => request('/purchase-orders', { method: 'POST', body: JSON.stringify(data) });
export const updatePurchaseOrder = (id: number, data: any) => request(`/purchase-orders/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const receivePurchaseOrder = (id: number, data: any) => request(`/purchase-orders/${id}/receive`, { method: 'POST', body: JSON.stringify(data) });

// Sales Orders
export const getSalesOrders = () => request('/sales-orders');
export const getSalesOrder = (id: number) => request(`/sales-orders/${id}`);
export const createSalesOrder = (data: any) => request('/sales-orders', { method: 'POST', body: JSON.stringify(data) });
export const fulfillSalesOrder = (id: number) => request(`/sales-orders/${id}/fulfill`, { method: 'POST' });

// Reports
export const getValuationReport = () => request('/reports/valuation');

// Dashboard
export const getDashboardSummary = () => request('/dashboard/summary');