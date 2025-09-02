'use client';

import { useQuery } from '@tanstack/react-query';
import { getDashboardSummary } from '@/lib/api';
import styles from './page.module.css';

function StatCard({ title, value }: { title: string, value: string | number }) {
  return (
    <div className={styles.card}>
      <h3 className={styles.cardTitle}>{title}</h3>
      <p className={styles.cardValue}>{value}</p>
    </div>
  );
}

export default function Home() {
  const { data: summary, isLoading, isError } = useQuery({
    queryKey: ['dashboardSummary'],
    queryFn: getDashboardSummary,
  });

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching dashboard data</div>;

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>Dashboard</h1>
        <div className={styles.grid}>
          <StatCard 
            title="Total Inventory Value" 
            value={`${summary.total_inventory_value.toFixed(2)}`}
          />
          <StatCard 
            title="Low Stock Items" 
            value={summary.low_stock_items_count} 
          />
          <StatCard 
            title="Open Purchase Orders" 
            value={summary.open_purchase_orders_count} 
          />
          <StatCard 
            title="Open Sales Orders" 
            value={summary.open_sales_orders_count} 
          />
        </div>
      </main>
    </div>
  );
}
