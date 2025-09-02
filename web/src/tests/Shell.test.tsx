import { render, screen } from '@testing-library/react';
import Shell from '@/components/layout/Shell';

describe('Shell', () => {
  it('renders the main heading', () => {
    render(<Shell><div>Test</div></Shell>);
    const heading = screen.getByRole('heading', { name: /inventory management/i });
    expect(heading).toBeInTheDocument();
  });
});
