# Web App Agent Guide

This directory contains the Next.js frontend. Follow these steps when modifying files here:

## Development
- This project uses **TypeScript** and **ESLint**. Ensure new code follows their conventions.
- Format source files with **Prettier** before committing.

## Testing
- Run `npm run lint` to check ESLint rules.
- Run unit tests with `npm test`.
- Run end-to-end tests with `npm run test:e2e` when changes might affect user flows.

## Environment
- Some tests require environment variables (e.g., API URLs, Sentry tokens). Create and populate a `.env.local` file before running tests.
- Ensure any required backend services are available when executing the end-to-end tests.
