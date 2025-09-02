'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { adjustStock } from '@/lib/api';
import styles from './ItemForm.module.css'; // Re-using the same styles

export default function AdjustStockForm({ item, onClose, onSuccess }: { item: any, onClose: () => void, onSuccess: () => void }) {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    quantity_change: 0,
    notes: '',
  });

  const adjustStockMutation = useMutation({
    mutationFn: (data: any) => adjustStock(item.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      onSuccess();
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    adjustStockMutation.mutate(formData);
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>Adjust Stock for {item.name}</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="number"
            name="quantity_change"
            value={formData.quantity_change}
            onChange={handleChange}
            placeholder="Quantity Change"
            required
          />
          <textarea
            name="notes"
            value={formData.notes}
            // @ts-ignore
            onChange={handleChange}
            placeholder="Notes (optional)"
          />
          <div className={styles.buttons}>
            <button type="submit" disabled={adjustStockMutation.isPending}>
              Adjust
            </button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}
