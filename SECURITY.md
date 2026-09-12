# Security Policy & Controls

## 1. Authentication & Session Management
- **Password Security:** Passwords hashed with bcrypt (`cost=12`) with salt generation.
- **JWT Architecture:** Short-lived access tokens (60 minutes) combined with long-lived refresh tokens (7 days).
- **Token Verification:** Cryptographic signature verification using HS256 algorithm with strict expiration checks.

## 2. Role-Based Access Control (RBAC)
- **Roles:** `CUSTOMER`, `SELLER`, `ADMIN`.
- **Backend Enforcement:** Protected routes enforce role guards via FastAPI dependency injection (`Depends(RoleChecker([...]))`). Frontend navigation hiding is treated strictly as a convenience, not a security control.
- **Data Isolation:** Multi-tenancy isolation ensures Sellers cannot access or modify records belonging to other sellers.

## 3. Data Protection & Validation
- **Input Validation:** All payloads are validated using Pydantic v2 schemas with explicit bounds and regex constraints.
- **SQL Injection Prevention:** 100% of database queries execute through SQLAlchemy ORM parameter binding.
- **Payment Information:** Payment card data is simulated with synthetic tokens; no real credit card numbers or banking secrets are ever accepted, processed, or persisted.
- **Secrets Management:** Secrets are injected strictly via `.env` environment variables. `.env` is ignored by version control.

## 4. Audit Logging
All security-sensitive operations generate structured audit log entries:
- Authentication events (Login, Logout, Failed attempts, Password updates).
- Authorization violations (Attempted privilege escalations).
- Financial events (Payments, Refunds, Order status updates).
- Catalog modifications (Product creation, status approval, inventory movements).
- Administrative actions (User suspension, seller verification).

Audit logs record `timestamp`, `user_id`, `action`, `resource_type`, `resource_id`, `ip_address`, and `status`. Passwords and authorization tokens are strictly filtered out.
