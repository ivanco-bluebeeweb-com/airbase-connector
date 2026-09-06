# Airbase Connector — Preparation

## Product Scope
Build a comprehensive Imperal connector for **Airbase** (Paylocity / Airbase Spend Management) under category **C29. Expense Management & Corporate Cards**. The integration connects directly to the official **Airbase REST APIs** (`https://api.airbase.io`), providing complete visibility and governance across corporate cards, out-of-pocket expenses, expense reports, spend policies, merchant categorization, employee reimbursements, and automated compliance auditing.

## Official API Specifications
- **API Architecture:** RESTful JSON API
- **Base URL:** `https://api.airbase.io`
- **Core Endpoints:**
  - `GET /v1/me` — verify token privileges and company context
  - `GET /v1/expenses` — list corporate expenses with cursor pagination
  - `GET /v1/expenses/{id}` — detailed single expense record
  - `GET /v1/cards` — virtual and physical spend cards
  - `GET /v1/reports` — aggregated expense reports and batches
  - `GET /v1/policies` — company spending limit and compliance policies
  - `GET /v1/merchants` — merchant classifications
  - `GET /v1/reimbursements` — employee reimbursement disbursements
- **Authentication Model:** Bearer Token via `Authorization: Bearer <api_key>`
- **Mandatory Requirements:**
  - Strict error classification: HTTP 429 rate limits with Retry-After extraction, HTTP 401/403 differentiation (Standard B8/B10).
  - Sanitization of Bearer tokens in error traces and diagnostic payloads (Standard B8).
  - Multi-tenant connection tracking and isolation via `connection_id` (Standard B9).

## Delivery Gates
1. [x] Official API discovery completed with Airbase REST API specifications.
2. [x] Core resource endpoints and Bearer auth verified.
3. [x] Five mandatory specification documents authored.
4. [x] Client implemented with B8-B10 compliance, secret redaction, and 429/401 classification.
5. [x] Panel sidebar implemented conforming to UI_INTERFACE_STANDARD.md.
6. [x] Verification of functions, imports, and Pydantic schemas.
