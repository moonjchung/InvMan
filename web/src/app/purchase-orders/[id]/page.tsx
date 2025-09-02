'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { getPurchaseOrder } from '@/lib/api';
import styles from '../PurchaseOrders.module.css'; // Re-using styles
import ReceivePOForm from '@/components/ReceivePOForm';
import PurchaseOrderForm from '@/components/PurchaseOrderForm';

export default function PurchaseOrderDetailPage() {
  const params = useParams();
  const id = parseInt(params.id as string, 10);
  const queryClient = useQueryClient();
  const [isReceiveModalOpen, setIsReceiveModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const { data: po, isLoading, isError } = useQuery({
    queryKey: ['purchaseOrder', id],
    queryFn: () => getPurchaseOrder(id),
    enabled: !!id,
  });

  const { data: user } = useQuery({ queryKey: ['user'] });

  const canManage = user && (user.role === 'admin' || user.role === 'manager');

  const handleOpenReceiveModal = () => {
    setIsReceiveModalOpen(true);
  };

  const handleCloseReceiveModal = () => {
    setIsReceiveModalOpen(false);
  };

  const handleReceiveSuccess = () => {
    handleCloseReceiveModal();
    queryClient.invalidateQueries({ queryKey: ['purchaseOrder', id] });
  };

  const handleOpenEditModal = () => {
    setIsEditModalOpen(true);
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
  };

  const handleEditSuccess = () => {
    handleCloseEditModal();
    queryClient.invalidateQueries({ queryKey: ['purchaseOrder', id] });
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching purchase order</div>;
  if (!po) return <div>Purchase order not found</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Purchase Order #{po.id}</h2>
        <div>
          {canManage && <button className={styles.editButton} onClick={handleOpenEditModal} disabled={po.status === 'COMPLETE'}>
            Edit PO
          </button>}
          <button className={styles.addButton} onClick={handleOpenReceiveModal} disabled={po.status === 'COMPLETE'}>
            Receive Items
          </button>
        </div>
      </div>
      <p><strong>Status:</strong> {po.status}</p>
      <p><strong>Supplier ID:</strong> {po.supplier_id}</p>
      <p><strong>Order Date:</strong> {po.order_date}</p>
      <p><strong>Expected Date:</strong> {po.expected_date}</p>

      <h3>Line Items</h3>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Quantity Ordered</th>
            <th>Quantity Received</th>
            <th>Unit Cost</th>
          </tr>
        </thead>
        <tbody>
          {po.line_items.map((li: any) => (
            <tr key={li.id}>
              <td>{li.item_id}</td>
              <td>{li.quantity_ordered}</td>
              <td>{li.quantity_received}</td>
              <td>{li.unit_cost}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {isReceiveModalOpen && (
        <ReceivePOForm
          po={po}
          onClose={handleCloseReceiveModal}
          onSuccess={handleReceiveSuccess}
        />
      )}

      {isEditModalOpen && (
        <PurchaseOrderForm
          purchaseOrder={po}
          onClose={handleCloseEditModal}
          onSuccess={handleEditSuccess}
        />
      )}
    </div>
  );
}
