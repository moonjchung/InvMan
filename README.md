# Inventory Management MVP

This is a production-ready, single-warehouse Inventory Management MVP built over an accelerated 6-week plan. It features a Python/FastAPI backend and a Next.js/TypeScript frontend.

## Tech Stack

*   **Backend:** FastAPI, Python, SQLAlchemy, Alembic, Poetry, SlowAPI (Rate Limiting), Apryse SDK & ReportLab (PDFs)
*   **Frontend:** Next.js, React, TypeScript, TanStack Query
*   **Database:** PostgreSQL (production-ready), SQLite (local development)
*   **Testing:** Pytest (API), Jest (Web), Playwright (E2E)
*   **Observability:** Sentry
*   **Deployment:** Vercel (Frontend), Railway (API) - as per plan

## Current Features (as of Week 6)

*   **Dashboard:** A main dashboard displaying key metrics:
    *   Total Inventory Value
    *   Count of Low-Stock Items
    *   Number of Open Purchase Orders
    *   Number of Open Sales Orders
*   **Item Management:** Full CRUD (Create, Read, Update, Delete) for items.
*   **Inventory Tracking:**
    *   Track stock levels for each item.
    *   Manually adjust stock levels with transaction logging.
*   **Data Management:**
    *   Bulk import items from a CSV file.
    *   Export all item data to a CSV file.
*   **Categories & Suppliers:** Full CRUD for managing item categories and suppliers.
*   **Purchase Orders (Receiving):**
    *   Create and manage Purchase Orders for suppliers.
    *   Receive items against a PO, with support for partial receipts.
    *   Stock levels are automatically updated upon receipt.
    *   **Barcode Scanning:** Use the device camera to scan item SKUs during the receiving process.
    *   **PDF Label Printing:** Generate and print 1" x 2.625" labels with product names and Code128 barcodes.
*   **Sales Orders (Issuing):**
    *   Create and manage Sales Orders for customers.
    *   Fulfill orders, which automatically decrements stock levels.
    *   **Negative Stock Prevention:** The system prevents creating or fulfilling orders for which there is insufficient stock.
*   **Reporting:**
    *   **Inventory Valuation Report:** A report showing the stock level, average cost, and total value for each item, with a grand total for the entire inventory. The average cost is calculated using the Moving Average method.
*   **Proactive Alerts:** Automatic low-stock email alerts are sent via Postmark when an item's stock level drops to or below its defined reorder point.
*   **Authentication:** JWT-based authentication for securing the API.

*   **Security & Hardening:**
    *   **Role-Based Access Control (RBAC):** API endpoints and UI actions are protected based on user roles (Admin, Manager, Staff).
    *   **API Rate Limiting:** The API is protected against brute-force and denial-of-service attacks with rate limiting.

*   **Observability & Testing:**
    *   **Sentry Integration:** Integrated for error and performance monitoring on both the backend and frontend.
    *   **End-to-End Testing:** Critical user flows are automatically tested using Playwright.

## Project Setup and Usage

Follow these instructions to get the application running locally.

### Prerequisites

*   Python 3.10+
*   Poetry (for Python package management)
*   Node.js and `npm`

### 1. Backend Setup (`/api`)

1.  **Navigate to the API directory:**
    ```bash
    cd api
    ```

2.  **Install Python dependencies using Poetry:**
    ```bash
    poetry install
    ```

3.  **Configure Environment Variables:**
    *   Copy the example `.env` file:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file and ensure the variables are set. For a quick start, the default `DATABASE_URL` points to a local SQLite file (`test.db`) and the `FIRST_SUPERUSER` credentials are pre-filled.

4.  **Run Database Migrations & Seed Data:**
    *   The seed script will automatically run all database migrations and then populate the database with a comprehensive set of demo data.
    ```bash
    poetry run python seed.py
    ```
    *   The default admin credentials are:
        *   **Email:** `admin@example.com`
        *   **Password:** `admin`

5.  **Run the Backend Server:**
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
    *   The API will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup (`/web`)

1.  **Navigate to the web directory:**
    ```bash
    cd web
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Environment Variables:**
    *   Copy the example `.env.example` file to `.env.local`:
        ```bash
        cp .env.example .env.local
        ```
    *   No changes are needed for local development.

4.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    *   The web application will be running at `http://localhost:3000`.

### 3. Using the Application

1.  Open your browser and go to `http://localhost:3000`.
2.  Log in with the admin credentials.
3.  Explore the application.

## Running Tests

### API Tests (Pytest)

1.  Navigate to the `/api` directory.
2.  Run the tests:
    ```bash
    poetry run pytest
    ```

### Web Tests (Jest)

1.  Navigate to the `/web` directory.
2.  Run the unit and component tests:
    ```bash
    npm test
    ```

### End-to-End Tests (Playwright)

1.  Make sure both the API and Web development servers are running.
2.  Navigate to the `/web` directory.
3.  Run the E2E tests:
    ```bash
    npx playwright test
    ```