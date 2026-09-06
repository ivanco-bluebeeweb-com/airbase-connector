"""Official Airbase REST API client aligned with api.airbase.io."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_AIRBASE_BASE = "https://api.airbase.io"

class AirbaseClient:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_AIRBASE_BASE).rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Airbase/0.1.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _sanitize_msg(self, msg: str) -> str:
        if not msg:
            return ""
        if self.api_key and len(self.api_key) > 6:
            msg = msg.replace(self.api_key, self.api_key[:3] + "..." + self.api_key[-3:])
        return msg

    def _classify_error(self, resp: httpx.Response, action_name: str) -> dict[str, Any]:
        status = resp.status_code
        err_msg = ""
        try:
            data = resp.json()
            if "errors" in data and isinstance(data["errors"], list) and len(data["errors"]) > 0:
                err_msg = "; ".join(e.get("message", "") for e in data["errors"])
            elif "message" in data:
                err_msg = data["message"]
            elif "error" in data:
                err_msg = str(data["error"])
        except Exception:
            err_msg = resp.text[:200]
        err_msg = self._sanitize_msg(err_msg)

        if status == 429:
            retry_after = resp.headers.get("Retry-After", "60")
            return {
                "status": "error",
                "code": "RATE_LIMITED",
                "message": f"Airbase API rate limit reached during {action_name}. Retry after {retry_after}s: {err_msg}",
                "retry_after": retry_after
            }
        elif status == 401:
            return {
                "status": "error",
                "code": "UNAUTHORIZED",
                "message": f"Invalid Airbase API Key or expired Bearer Token during {action_name}: {err_msg}"
            }
        elif status == 403:
            return {
                "status": "error",
                "code": "FORBIDDEN",
                "message": f"Insufficient Airbase scopes/permissions for {action_name}: {err_msg}"
            }
        elif status == 404:
            return {
                "status": "error",
                "code": "NOT_FOUND",
                "message": f"Airbase resource not found during {action_name}: {err_msg}"
            }
        return {
            "status": "error",
            "code": f"HTTP_{status}",
            "message": f"Airbase API error ({status}) during {action_name}: {err_msg}"
        }

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/users/me", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "verify_auth")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_expenses(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/expenses", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_expenses")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_expense(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/expenses/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_expense(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/expenses", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_expense")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_expense(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/expenses/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_expense(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/expenses/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_expense({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_cards(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/cards", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_cards")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_card(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/cards/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_card(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/cards", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_card")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_card(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/cards/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_card(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/cards/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_card({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_reports(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/reports", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_reports")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_report(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/reports/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_report(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/reports", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_report")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_report(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/reports/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_report(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/reports/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_report({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_policies(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/policies", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_policies")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_policy(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/policies/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_policy(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/policies", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_policy")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_policy(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/policies/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_policy(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/policies/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_policy({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_merchants(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/merchants", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_merchants")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_merchant(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/merchants/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_merchant(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/merchants", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_merchant")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_merchant(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/merchants/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_merchant(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/merchants/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_merchant({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def list_reimbursements(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/reimbursements", headers=self.headers, params=params)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, "list_reimbursements")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def get_reimbursement(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/v1/reimbursements/{item_id}", headers=self.headers)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"get_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def create_reimbursement(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        payload = {"name": name, **(details or {})}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.post(f"{self.base_url}/v1/reimbursements", headers=self.headers, json=payload)
                if resp.status_code in (200, 201):
                    return resp.json()
                return self._classify_error(resp, "create_reimbursement")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def update_reimbursement(self, item_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.patch(f"{self.base_url}/v1/reimbursements/{item_id}", headers=self.headers, json=fields)
                if resp.status_code == 200:
                    return resp.json()
                return self._classify_error(resp, f"update_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}

    async def delete_reimbursement(self, item_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/v1/reimbursements/{item_id}", headers=self.headers)
                if resp.status_code in (200, 204):
                    return {"deleted": True, "id": item_id}
                return self._classify_error(resp, f"delete_reimbursement({item_id})")
            except Exception as e:
                return {"status": "error", "code": "NETWORK_ERROR", "message": self._sanitize_msg(str(e))}
