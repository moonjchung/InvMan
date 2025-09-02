'use client';

import { useQuery } from '@tanstack/react-query';
import { getValuationReport } from '@/lib/api';
import styles from './Valuation.module.css';

export default function ValuationPage() {
  const { data: report, isLoading, isError } = useQuery({
    queryKey: ['valuationReport'],
    queryFn: getValuationReport,
  });

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching valuation report</div>;

  const totalValue = report.reduce((acc: number, item: any) => acc + item.total_value, 0);

  return (
    <div className={styles.container}>
      <h2>Inventory Valuation Report</h2>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Stock Level</th>
            <th>Average Cost</th>
            <th>Total Value</th>
          </tr>
        </thead>
        <tbody>
          {report.map((item: any) => (
            <tr key={item.item_id}>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.stock_level}</td>
              <td>{item.average_cost.toFixed(2)}</td>
              <td>{item.total_value.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={4} style={{ textAlign: 'right' }}><strong>Total Inventory Value:</strong></td>
            <td><strong>{totalValue.toFixed(2)}</strong></td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
