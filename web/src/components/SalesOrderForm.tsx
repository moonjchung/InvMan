'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getItems, createSalesOrder } from '@/lib/api';
import styles from './ItemForm.module.css'; // Re-using styles

export default function SalesOrderForm({ onClose, onSuccess }: { onClose: () => void, onSuccess: () => void }) {
  const queryClient = useQueryClient();
  const [customerName, setCustomerName] = useState('');
  const [orderDate, setOrderDate] = useState('');
  const [lineItems, setLineItems] = useState([{ item_id: '', quantity_ordered: 1, unit_price: 0 }]);

  const { data: items } = useQuery({ queryKey: ['items'], queryFn: getItems });

  const createMutation = useMutation({
    mutationFn: createSalesOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['salesOrders'] });
      onSuccess();
    },
  });

  const handleLineItemChange = (index: number, field: string, value: any) => {
    const updatedLineItems = [...lineItems];
    updatedLineItems[index][field] = value;
    setLineItems(updatedLineItems);
  };

  const addLineItem = () => {
    setLineItems([...lineItems, { item_id: '', quantity_ordered: 1, unit_price: 0 }]);
  };

  const removeLineItem = (index: number) => {
    const updatedLineItems = [...lineItems];
    updatedLineItems.splice(index, 1);
    setLineItems(updatedLineItems);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const soData = {
      customer_name: customerName,
      order_date: orderDate,
      line_items: lineItems.map(li => ({ ...li, item_id: parseInt(li.item_id), unit_price: parseFloat(li.unit_price) })),
    };
    createMutation.mutate(soData);
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>Create Sales Order</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" value={customerName} onChange={(e) => setCustomerName(e.target.value)} placeholder="Customer Name" required />
          <input type="date" value={orderDate} onChange={(e) => setOrderDate(e.target.value)} required />

          <h3>Line Items</h3>
          {lineItems.map((li, index) => (
            <div key={index} className={styles.lineItem}>
              <select value={li.item_id} onChange={(e) => handleLineItemChange(index, 'item_id', e.target.value)} required>
                <option value="">Select Item</option>
                {items?.map((i: any) => <option key={i.id} value={i.id}>{i.name}</option>)}
              </select>
              <input type="number" value={li.quantity_ordered} onChange={(e) => handleLineItemChange(index, 'quantity_ordered', parseInt(e.target.value))} min="1" required />
              <input type="number" value={li.unit_price} onChange={(e) => handleLineItemChange(index, 'unit_price', parseFloat(e.target.value))} min="0" step="0.01" required />
              <button type="button" onClick={() => removeLineItem(index)}>Remove</button>
            </div>
          ))}
          <button type="button" onClick={addLineItem}>Add Line Item</button>

          <div className={styles.buttons}>
            <button type="submit" disabled={createMutation.isPending}>Create</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
