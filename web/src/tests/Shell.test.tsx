import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Shell from '@/components/layout/Shell';

jest.mock('@/lib/api', () => ({
  getUsersMe: jest.fn().mockResolvedValue({ id: 1, role: 'user' }),
}));

describe('Shell', () => {
  it('renders the main heading', () => {
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    render(
      <QueryClientProvider client={queryClient}>
        <Shell>
          <div>Test</div>
        </Shell>
      </QueryClientProvider>,
    );
    const heading = screen.getByRole('heading', {
      name: /inventory management/i,
    });
    expect(heading).toBeInTheDocument();
  });
});
