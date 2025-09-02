'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getItems, deleteItem, exportItemsCsv } from '@/lib/api';
import styles from './Items.module.css';
import ItemForm from '@/components/ItemForm';
import AdjustStockForm from '@/components/AdjustStockForm';
import ImportCsvForm from '@/components/ImportCsvForm';

export default function ItemsPage() {
  const queryClient = useQueryClient();
  const [isItemFormOpen, setIsItemFormOpen] = useState(false);
  const [isAdjustStockFormOpen, setIsAdjustStockFormOpen] = useState(false);
  const [isImportCsvFormOpen, setIsImportCsvFormOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const { data: items, isLoading, isError } = useQuery({
    queryKey: ['items'],
    queryFn: getItems,
  });

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const deleteMutation = useMutation({
    mutationFn: deleteItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });

  const handleDelete = (id: number) => {
    deleteMutation.mutate(id);
  };

  const handleAdd = () => {
    setSelectedItem(null);
    setIsItemFormOpen(true);
  };

  const handleEdit = (item: any) => {
    setSelectedItem(item);
    setIsItemFormOpen(true);
  };

  const handleAdjustStock = (item: any) => {
    setSelectedItem(item);
    setIsAdjustStockFormOpen(true);
  };

  const handleImport = () => {
    setIsImportCsvFormOpen(true);
  };

  const handleCloseModals = () => {
    setIsItemFormOpen(false);
    setIsAdjustStockFormOpen(false);
    setIsImportCsvFormOpen(false);
    setSelectedItem(null);
  };

  const handleSuccess = () => {
    handleCloseModals();
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching items</div>;

  return (
    <div className={styles.container}>
      <h2>Items</h2>
      <div className={styles.buttonGroup}>
        {canManage && <button className={styles.addButton} onClick={handleAdd}>Add Item</button>}
        {canManage && <button className={styles.importButton} onClick={handleImport}>Import from CSV</button>}
        {canManage && <button className={styles.exportButton} onClick={exportItemsCsv}>Export to CSV</button>}
      </div>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Stock Level</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item: any) => (
            <tr key={item.id}>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.stock_level}</td>
              <td>{item.price}</td>
              <td>
                {canManage && <button className={styles.editButton} onClick={() => handleEdit(item)}>Edit</button>}
                {canManage && <button className={styles.deleteButton} onClick={() => handleDelete(item.id)} disabled={deleteMutation.isPending}>
                  {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
                </button>}
                <button className={styles.adjustButton} onClick={() => handleAdjustStock(item)}>Adjust Stock</button>
                <a href={`${process.env.NEXT_PUBLIC_API_BASE_URL}/items/${item.id}/label.pdf`} target="_blank" rel="noopener noreferrer">
                  <button className={styles.printButton}>Print Label</button>
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {isItemFormOpen && (
        <ItemForm 
          item={selectedItem} 
          onClose={handleCloseModals} 
          onSuccess={handleSuccess} 
        />
      )}
      {isAdjustStockFormOpen && (
        <AdjustStockForm 
          item={selectedItem} 
          onClose={handleCloseModals} 
          onSuccess={handleSuccess} 
        />
      )}
      {isImportCsvFormOpen && (
        <ImportCsvForm 
          onClose={handleCloseModals} 
          onSuccess={handleSuccess} 
        />
      )}
    </div>
  );
}