import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('renders input and submit button', () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Enter your query.../i);
  const buttonElement = screen.getByText(/Submit/i);
  expect(inputElement).toBeInTheDocument();
  expect(buttonElement).toBeInTheDocument();
});

test('handles user input and submission', async () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Enter your query.../i);
  const buttonElement = screen.getByText(/Submit/i);

  fireEvent.change(inputElement, { target: { value: 'test query' } });
  expect(inputElement.value).toBe('test query');

  fireEvent.click(buttonElement);
  // Add mock fetch logic here if needed
});
