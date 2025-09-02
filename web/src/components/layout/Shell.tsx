'use client';

import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';
import { getUsersMe } from '@/lib/api';
import styles from './Shell.module.css';

export default function Shell({ children }: { children: React.ReactNode }) {
  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: getUsersMe,
  });

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <h1>Inventory Management</h1>
      </header>
      <div className={styles.container}>
        <nav className={styles.sidebar}>
          <ul>
            <li>
              <Link href="/">Dashboard</Link>
            </li>
            <li>
              <Link href="/items">Items</Link>
            </li>
            <li>
              <Link href="/categories">Categories</Link>
            </li>
            <li>
              <Link href="/suppliers">Suppliers</Link>
            </li>
            <li>
              <Link href="/purchase-orders">Purchase Orders</Link>
            </li>
            <li>
              <Link href="/sales-orders">Sales Orders</Link>
            </li>
            <li className={styles.separator}>Reports</li>
            <li>
              <Link href="/reports/valuation">Valuation</Link>
            </li>
            {user && user.role === 'admin' && (
              <li>
                <Link href="/settings">Settings</Link>
              </li>
            )}
          </ul>
        </nav>
        <main className={styles.main}>{children}</main>
      </div>
    </div>
  );
}