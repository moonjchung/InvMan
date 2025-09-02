'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { receivePurchaseOrder, getItemBySku } from '@/lib/api';
import styles from './ItemForm.module.css'; // Re-using styles
import BarcodeScanner from './BarcodeScanner';

export default function ReceivePOForm({ po, onClose, onSuccess }: { po: any, onClose: () => void, onSuccess: () => void }) {
  const queryClient = useQueryClient();
  const [receivedItems, setReceivedItems] = useState(
    po.line_items.map((li: any) => ({ id: li.id, quantity: 0 }))
  );

  const receiveMutation = useMutation({
    mutationFn: (data: any) => receivePurchaseOrder(po.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['purchaseOrder', po.id] });
      queryClient.invalidateQueries({ queryKey: ['purchaseOrders'] });
      onSuccess();
    },
  });

  const handleChange = (index: number, value: number) => {
    const updatedItems = [...receivedItems];
    updatedItems[index].quantity = value;
    setReceivedItems(updatedItems);
  };

  const handleScan = async (sku: string) => {
    try {
      const item = await getItemBySku(sku);
      if (item) {
        const lineItemIndex = po.line_items.findIndex((li: any) => li.item_id === item.id);
        if (lineItemIndex !== -1) {
          const updatedItems = [...receivedItems];
          updatedItems[lineItemIndex].quantity += 1;
          setReceivedItems(updatedItems);
        }
      }
    } catch (error) {
      console.error('Error fetching item by SKU', error);
      // Handle item not found error
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    receiveMutation.mutate(receivedItems);
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>Receive Items for PO #{po.id}</h2>
        <BarcodeScanner onScan={handleScan} />
        <form onSubmit={handleSubmit}>
          {po.line_items.map((li: any, index: number) => (
            <div key={li.id} className={styles.lineItem}>
              <span>Item ID: {li.item_id} (Ordered: {li.quantity_ordered}, Received: {li.quantity_received})</span>
              <input
                type="number"
                value={receivedItems[index].quantity}
                onChange={(e) => handleChange(index, parseInt(e.target.value, 10))}
                min="0"
                max={li.quantity_ordered - li.quantity_received}
              />
            </div>
          ))}
          <div className={styles.buttons}>
            <button type="submit" disabled={receiveMutation.isPending}>Receive</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}