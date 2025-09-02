'use client';

import { useParams } from 'next/navigation';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getSalesOrder, fulfillSalesOrder } from '@/lib/api';
import styles from '../SalesOrders.module.css'; // Re-using styles

export default function SalesOrderDetailPage() {
  const params = useParams();
  const id = parseInt(params.id as string, 10);
  const queryClient = useQueryClient();

  const { data: so, isLoading, isError } = useQuery({
    queryKey: ['salesOrder', id],
    queryFn: () => getSalesOrder(id),
    enabled: !!id,
  });

  const fulfillMutation = useMutation({
    mutationFn: () => fulfillSalesOrder(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['salesOrder', id] });
      queryClient.invalidateQueries({ queryKey: ['salesOrders'] });
    },
  });

  const handleFulfill = () => {
    fulfillMutation.mutate();
  };

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching sales order</div>;
  if (!so) return <div>Sales order not found</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Sales Order #{so.id}</h2>
        <button onClick={handleFulfill} disabled={so.status !== 'CONFIRMED' || fulfillMutation.isPending}>
          Fulfill Order
        </button>
      </div>
      <p><strong>Customer:</strong> {so.customer_name}</p>
      <p><strong>Status:</strong> {so.status}</p>
      <p><strong>Order Date:</strong> {so.order_date}</p>

      <h3>Line Items</h3>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Item ID</th>
            <th>Quantity Ordered</th>
            <th>Unit Price</th>
          </tr>
        </thead>
        <tbody>
          {so.line_items.map((li: any) => (
            <tr key={li.id}>
              <td>{li.item_id}</td>
              <td>{li.quantity_ordered}</td>
              <td>{li.unit_price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
