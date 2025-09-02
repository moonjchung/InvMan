'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getPurchaseOrders } from '@/lib/api';
import styles from './PurchaseOrders.module.css';
import PurchaseOrderForm from '@/components/PurchaseOrderForm';

export default function PurchaseOrdersPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data: purchaseOrders, isLoading, isError } = useQuery({
    queryKey: ['purchaseOrders'],
    queryFn: getPurchaseOrders,
  });

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const handleAdd = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleSuccess = () => {
    handleCloseModal();
    queryClient.invalidateQueries({ queryKey: ['purchaseOrders'] });
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching purchase orders</div>;

  return (
    <div className={styles.container}>
      <h2>Purchase Orders</h2>
      {canManage && <button className={styles.addButton} onClick={handleAdd}>Add Purchase Order</button>}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Supplier ID</th>
            <th>Status</th>
            <th>Order Date</th>
            <th>Expected Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {purchaseOrders.map((po: any) => (
            <tr key={po.id}>
              <td>{po.id}</td>
              <td>{po.supplier_id}</td>
              <td>{po.status}</td>
              <td>{po.order_date}</td>
              <td>{po.expected_date}</td>
              <td>
                <Link href={`/purchase-orders/${po.id}`}>
                  <button className={styles.editButton}>View</button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {isModalOpen && (
        <PurchaseOrderForm 
          onClose={handleCloseModal} 
          onSuccess={handleSuccess} 
        />
      )}
    </div>
  );
}
