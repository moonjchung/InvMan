'use client';

import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { getSalesOrders } from '@/lib/api';
import styles from './SalesOrders.module.css';
import SalesOrderForm from '@/components/SalesOrderForm';

export default function SalesOrdersPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const { data: salesOrders, isLoading, isError } = useQuery({
    queryKey: ['salesOrders'],
    queryFn: getSalesOrders,
  });

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
    queryClient.invalidateQueries({ queryKey: ['salesOrders'] });
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching sales orders</div>;

  return (
    <div className={styles.container}>
      <h2>Sales Orders</h2>
      {canManage && <button className={styles.addButton} onClick={handleAdd}>Add Sales Order</button>}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer</th>
            <th>Status</th>
            <th>Order Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {salesOrders.map((so: any) => (
            <tr key={so.id}>
              <td>{so.id}</td>
              <td>{so.customer_name}</td>
              <td>{so.status}</td>
              <td>{so.order_date}</td>
              <td>
                <Link href={`/sales-orders/${so.id}`}>
                  <button className={styles.editButton}>View</button>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {isModalOpen && (
        <SalesOrderForm 
          onClose={handleCloseModal} 
          onSuccess={handleSuccess} 
        />
      )}
    </div>
  );
}