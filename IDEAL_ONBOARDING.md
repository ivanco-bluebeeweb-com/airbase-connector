# Airbase Connector — Ideal Onboarding Walkthrough

1. **Obtain API Token:**
   - Log in to Airbase (app.airbase.io).
   - Go to **Settings > Integrations > API & Webhooks**.
   - Create an API Key with `expenses:read`, `cards:manage`, `reports:read` permissions.
2. **Connect in Imperal:**
   - Open Airbase Connector in Imperal Cloud.
   - Enter Connection Label (e.g., `Acme Airbase`).
   - Paste API Token.
   - Click **Connect Airbase**.
3. **Verify Health:**
   - Execute `audit_spend_compliance` or `get_spend_overview` to confirm live connection.
