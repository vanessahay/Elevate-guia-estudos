# STRIDE Threat Model Assessment: `shopping-assistant`

## System Architecture & Boundaries

```
[ Customer / A2A Client ]
          │
          ▼
 [ FastAPI Gateway (app/fast_api_app.py) ]
          │
          ▼
 [ ADK Runner & Root Agent (shopping_assistant) ]
          │
          ▼
 [ Tool: redeem_discount_code(code, user_id) ]
          │
          ▼
 [ In-Memory Stores (DISCOUNT_CODES, REDEEMED_CODES) ]
```

- **Entry Points**: FastAPI REST endpoints, A2A RPC routes (`/a2a/app`), and ADK agent prompt loop.
- **Tools**: `redeem_discount_code(code: str, user_id: str)`.
- **Data Layers**: In-memory state (`DISCOUNT_CODES` dict and `REDEEMED_CODES` set).

---

## STRIDE Evaluation

| Pillar | Risk Assessment & Vulnerability | Severity | Mitigation Strategy |
| :--- | :--- | :---: | :--- |
| **Spoofing** | **Unverified User Identity**: `redeem_discount_code` trusts `user_id` passed as an string argument from LLM prompt inputs without validating session identity. An attacker can impersonate any user ID. | **High** | Bind `user_id` to authenticated session context/JWT claims rather than LLM tool arguments. |
| **Tampering** | **Ephemeral State Loss & Race Conditions**: `REDEEMED_CODES` relies on an in-memory set. Service restarts reset redemption state, and multi-instance deployments allow race conditions / double redemptions. | **Medium** | Store redemption records in an atomic datastore (e.g. Cloud SQL / Redis) with transactional locks. |
| **Repudiation** | **Missing Audit Logs**: Successful or failed code redemptions return plain strings without writing structured audit logs (recording IP, timestamp, user ID, code). | **Medium** | Integrate structured logging (`google-cloud-logging`) for all sensitive financial/discount actions. |
| **Information Disclosure** | **Hardcoded API Key**: `app/agent.py` contains a hardcoded API key (`api_key="AIzaSyD-mock-key-value-12345"`). | **High** | Remove hardcoded secrets, load from `GEMINI_API_KEY` env var, and enforce Semgrep pre-commit gating. |
| **Denial of Service** | **Brute-Force & Unbounded Inputs**: No rate limiting or string length validation on discount code queries, allowing automated code guessing attacks. | **Medium** | Apply rate limits on FastAPI routes and enforce input validation via Pydantic schemas. |
| **Elevation of Privilege** | **Missing Action Authorization**: Any user who can query the agent can attempt discount redemptions regardless of account status or authorization tier. | **High** | Implement role-based access control (RBAC) and authorization checks before executing tool logic. |

---

## Priority Action Plan

1. **Secret Hygiene**: Remove `api_key` string from `app/agent.py` and rely on environment variables.
2. **Pydantic Tool Input Validation**: Wrap tool parameters in Pydantic models as specified in `.agents/CONTEXT.md`.
3. **Session-Bound Identity**: Extract authenticated user identity from context instead of unverified arguments.
4. **Persistent & Transactional Store**: Replace in-memory sets with database-backed atomic operations.
