'use client';

import { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createItem, updateItem } from '@/lib/api';
import styles from './ItemForm.module.css';

export default function ItemForm({ item, onClose, onSuccess }: { item?: any, onClose: () => void, onSuccess: () => void }) {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    sku: '',
    name: '',
    stock_level: 0,
    price: 0,
  });

  useEffect(() => {
    if (item) {
      setFormData({
        sku: item.sku,
        name: item.name,
        stock_level: item.stock_level,
        price: item.price,
      });
    }
  }, [item]);

  const createMutation = useMutation({
    mutationFn: createItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      onSuccess();
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: any) => updateItem(item.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      onSuccess();
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (item) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>{item ? 'Edit Item' : 'Add Item'}</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="sku" value={formData.sku} onChange={handleChange} placeholder="SKU" required />
          <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Name" required />
          <input type="number" name="stock_level" value={formData.stock_level} onChange={handleChange} placeholder="Stock Level" required />
          <input type="number" name="price" value={formData.price} onChange={handleChange} placeholder="Price" required />
          <div className={styles.buttons}>
            <button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
              {item ? 'Update' : 'Create'}
            </button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}