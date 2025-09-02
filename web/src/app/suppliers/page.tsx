'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getSuppliers, deleteSupplier } from '@/lib/api';
import styles from './Suppliers.module.css';
import SupplierForm from '@/components/SupplierForm';

export default function SuppliersPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedSupplier, setSelectedSupplier] = useState(null);

  const { data: suppliers, isLoading, isError } = useQuery({
    queryKey: ['suppliers'],
    queryFn: getSuppliers,
  });

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const deleteMutation = useMutation({
    mutationFn: deleteSupplier,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['suppliers'] });
    },
  });

  const handleDelete = (id: number) => {
    deleteMutation.mutate(id);
  };

  const handleAdd = () => {
    setSelectedSupplier(null);
    setIsModalOpen(true);
  };

  const handleEdit = (supplier: any) => {
    setSelectedSupplier(supplier);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedSupplier(null);
  };

  const handleSuccess = () => {
    handleCloseModal();
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching suppliers</div>;

  return (
    <div className={styles.container}>
      <h2>Suppliers</h2>
      {canManage && <button className={styles.addButton} onClick={handleAdd}>Add Supplier</button>}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {suppliers.map((supplier: any) => (
            <tr key={supplier.id}>
              <td>{supplier.id}</td>
              <td>{supplier.name}</td>
              <td>
                {canManage && <>
                  <button className={styles.editButton} onClick={() => handleEdit(supplier)}>Edit</button>
                  <button 
                    className={styles.deleteButton} 
                    onClick={() => handleDelete(supplier.id)}
                    disabled={deleteMutation.isPending}
                  >
                    {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
                  </button>
                </>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {isModalOpen && (
        <SupplierForm 
          supplier={selectedSupplier} 
          onClose={handleCloseModal} 
          onSuccess={handleSuccess} 
        />
      )}
    </div>
  );
}
