# Airbase Connector — Auth & Credentials Standard (B1–B10)

## Authentication Architecture
- **Method:** Bearer Token (API Key)
- **Token Delivery:** `Authorization: Bearer <api_key>` HTTP Header
- **Secret Storage:** Vault-backed encrypted storage under `airbase_connections`
- **Masking:** First 4 and last 4 characters visible (`abcd…wxyz`), middle redacted.

## Error Handling & Reliability (B8 & B10)
- **HTTP 429 Rate Limiting:** Returns structured `RATE_LIMITED` error with `Retry-After` seconds.
- **HTTP 401 / 403:** Classified into `UNAUTHORIZED` and `FORBIDDEN` without generic crash.
- **Secret Sanitization:** All raw tokens stripped from error logs and diagnostic payloads before return.
- **Tenant Isolation (B9):** Each tenant request isolated by `connection_id`.
