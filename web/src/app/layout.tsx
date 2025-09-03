import type { Metadata } from 'next';
import './globals.css';
import Shell from '@/components/layout/Shell';
import QueryProvider from '@/components/QueryProvider';

export const metadata: Metadata = {
  title: 'Inventory Management',
  description: 'Inventory Management App',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>
          <Shell>{children}</Shell>
        </QueryProvider>
      </body>
    </html>
  );
}