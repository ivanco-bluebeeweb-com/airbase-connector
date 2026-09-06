# Airbase Connector — Connector Discovery

## Target System & Architecture
- **Vendor:** Airbase (Airbase Spend Management)
- **Primary Domain:** Spend management, corporate cards, accounts payable automation, expense reimbursements.
- **Protocol:** HTTPS RESTful JSON API
- **Base URL:** `https://api.airbase.io`
- **Authentication Scheme:** Bearer Token via `Authorization: Bearer <api_key>`

## Supported Resource Matrix
1. **Cards**: Corporate virtual and physical cards (`/v1/cards`).
2. **Expenses**: Employee out-of-pocket and card transactions (`/v1/expenses`).
3. **Reports**: Aggregated expense reports for manager approval (`/v1/reports`).
4. **Policies**: Spend limit and travel compliance policies (`/v1/policies`).
5. **Merchants**: Categorization of vendors and merchants (`/v1/merchants`).
6. **Reimbursements**: Direct bank disbursements to workers (`/v1/reimbursements`).
7. **Audits**: `audit_spend_compliance` & `get_spend_overview` automated auditing algorithms.
