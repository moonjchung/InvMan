# Architecture

## Security

### Role-Based Access Control (RBAC)

The API enforces role-based permissions for all actions. The roles are defined as follows:

*   **Admin:** Can perform all actions, including user management and system settings.
*   **Manager:** Can perform most inventory-related actions, including creating and updating items, categories, suppliers, purchase orders, and sales orders.
*   **Staff:** Can view most data and perform operational tasks like adjusting stock, receiving purchase orders, and fulfilling sales orders.

### HTTPS

TLS termination and HTTPS enforcement are the responsibility of the hosting platforms (Railway for the API, Vercel for the web app) and are configured by default on those platforms.
