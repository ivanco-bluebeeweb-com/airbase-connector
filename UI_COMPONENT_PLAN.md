# Airbase Connector — UI Component Plan

## Left Sidebar Layout (`panels.py`)
- **Container:** `ui.Stack(direction="v", gap=3, align="stretch")`
- **Header:** Title "Airbase", descriptive caption.
- **Connection Form:**
  - `ui.Input(name="api_key", placeholder="Enter Airbase API token...", password=True)`
  - `ui.Button("Connect Airbase", variant="primary", size="sm")`
- **Help Section:**
  - `ui.Modal` with guided step-by-step setup instructions.
- **Settings Link:**
  - Secondary button opening `__airbase_settings` panel.
