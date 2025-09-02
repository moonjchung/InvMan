'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getSuppliers, getItems, createPurchaseOrder, updatePurchaseOrder } from '@/lib/api';
import styles from './ItemForm.module.css'; // Re-using the same styles

export default function PurchaseOrderForm({ purchaseOrder, onClose, onSuccess }: { purchaseOrder?: any, onClose: () => void, onSuccess: () => void }) {
  const queryClient = useQueryClient();
  const [supplierId, setSupplierId] = useState('');
  const [orderDate, setOrderDate] = useState('');
  const [expectedDate, setExpectedDate] = useState('');
  const [status, setStatus] = useState('DRAFT');
  const [lineItems, setLineItems] = useState([{ item_id: '', quantity_ordered: 1, unit_cost: 0 }]);

  const { data: suppliers } = useQuery({ queryKey: ['suppliers'], queryFn: getSuppliers });
  const { data: items } = useQuery({ queryKey: ['items'], queryFn: getItems });

  useEffect(() => {
    if (purchaseOrder) {
      setSupplierId(purchaseOrder.supplier_id);
      setOrderDate(purchaseOrder.order_date);
      setExpectedDate(purchaseOrder.expected_date);
      setStatus(purchaseOrder.status);
      setLineItems(purchaseOrder.line_items);
    }
  }, [purchaseOrder]);

  const createMutation = useMutation({
    mutationFn: createPurchaseOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['purchaseOrders'] });
      onSuccess();
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: any) => updatePurchaseOrder(purchaseOrder.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['purchaseOrders'] });
      queryClient.invalidateQueries({ queryKey: ['purchaseOrder', purchaseOrder.id] });
      onSuccess();
    },
  });

  const handleLineItemChange = (index: number, field: string, value: any) => {
    const updatedLineItems = [...lineItems];
    updatedLineItems[index][field] = value;
    setLineItems(updatedLineItems);
  };

  const addLineItem = () => {
    setLineItems([...lineItems, { item_id: '', quantity_ordered: 1, unit_cost: 0 }]);
  };

  const removeLineItem = (index: number) => {
    const updatedLineItems = [...lineItems];
    updatedLineItems.splice(index, 1);
    setLineItems(updatedLineItems);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const poData = {
      supplier_id: parseInt(supplierId),
      order_date: orderDate,
      expected_date: expectedDate,
      status: status,
      line_items: lineItems.map(li => ({ ...li, item_id: parseInt(li.item_id) })),
    };
    if (purchaseOrder) {
      updateMutation.mutate(poData);
    } else {
      createMutation.mutate(poData);
    }
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>{purchaseOrder ? 'Edit Purchase Order' : 'Create Purchase Order'}</h2>
        <form onSubmit={handleSubmit}>
          <select value={supplierId} onChange={(e) => setSupplierId(e.target.value)} required>
            <option value="">Select Supplier</option>
            {suppliers?.map((s: any) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          <input type="date" value={orderDate} onChange={(e) => setOrderDate(e.target.value)} required />
          <input type="date" value={expectedDate} onChange={(e) => setExpectedDate(e.target.value)} required />
          <input type="text" value={status} onChange={(e) => setStatus(e.target.value)} required />

          <h3>Line Items</h3>
          {lineItems.map((li, index) => (
            <div key={index} className={styles.lineItem}>
              <select value={li.item_id} onChange={(e) => handleLineItemChange(index, 'item_id', e.target.value)} required>
                <option value="">Select Item</option>
                {items?.map((i: any) => <option key={i.id} value={i.id}>{i.name}</option>)}
              </select>
              <input type="number" value={li.quantity_ordered} onChange={(e) => handleLineItemChange(index, 'quantity_ordered', parseInt(e.target.value))} min="1" required />
              <input type="number" value={li.unit_cost} onChange={(e) => handleLineItemChange(index, 'unit_cost', parseFloat(e.target.value))} min="0" step="0.01" required />
              <button type="button" onClick={() => removeLineItem(index)}>Remove</button>
            </div>
          ))}
          <button type="button" onClick={addLineItem}>Add Line Item</button>

          <div className={styles.buttons}>
            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
              {purchaseOrder ? 'Update' : 'Create'}
            </button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}