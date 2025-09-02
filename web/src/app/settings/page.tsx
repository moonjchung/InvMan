'use client';

import { useQuery } from '@tanstack/react-query';
import { getSettings, getUsersMe } from '@/lib/api';
import styles from './Settings.module.css';

export default function SettingsPage() {
  const { data: user, isLoading: isLoadingUser } = useQuery({
    queryKey: ['user'],
    queryFn: getUsersMe,
  });

  const { data: settings, isLoading: isLoadingSettings } = useQuery({
    queryKey: ['settings'],
    queryFn: getSettings,
    enabled: !!user && user.role === 'admin',
  });

  if (isLoadingUser) {
    return <div>Loading user...</div>;
  }

  if (!user || user.role !== 'admin') {
    return <div className={styles.container}>Access Denied</div>;
  }

  if (isLoadingSettings) {
    return <div className={styles.container}>Loading settings...</div>;
  }

  return (
    <div className={styles.container}>
      <h2>Settings</h2>
      <table className={styles.table}>
        <tbody>
          <tr>
            <th>App Name</th>
            <td>{settings.app_name}</td>
          </tr>
          <tr>
            <th>Environment</th>
            <td>{settings.environment}</td>
          </tr>
          <tr>
            <th>API Version</th>
            <td>{settings.api_version}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
