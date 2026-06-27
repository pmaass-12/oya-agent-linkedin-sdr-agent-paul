import os
import json
import urllib.parse
import urllib.request
import urllib.error

# Oya skill: read/write the Show.IO CRM.
# Reads INPUT_JSON (the agent's call args) and credentials from the env.
#
# Credentials (set when adding the skill to an agent):
#   SHOWIO_API_KEY   – the CRM_AGENT_API_KEY value from Show.IO
#   SHOWIO_BASE_URL  – optional, defaults to https://app.tryshow.io
#
# INPUT_JSON:
#   { "action": "upsert_lead" | "upsert_account" | "list_conferences", ...args }
#   upsert_lead fields:    email, name|first_name|last_name, company_name,
#                          title, phone, linkedin_url, location, status, note, source
#   upsert_account fields: name (required), website, industry, description,
#                          linkedin_url, location, revenue_range, employee_count, phone
#   list_conferences args: q (optional search), limit (optional)  → READ, returns
#                          the conferences already tracked in the CRM (for dedupe).

# action -> (HTTP method, path)
ROUTES = {
    "upsert_lead":       ("POST", "/api/agent/crm/leads"),
    "upsert_account":    ("POST", "/api/agent/crm/accounts"),
    "list_conferences":  ("GET",  "/api/agent/crm/conferences"),
    "list_leads":          ("GET",  "/api/agent/crm/leads"),
    "create_conference":   ("POST", "/api/agent/crm/conferences"),
    "exhibitors_from_url": ("POST", "/api/agent/crm/exhibitors-from-url"),
    "notify":              ("POST", "/api/agent/crm/notify"),
}


VALID_ACTIONS = set(ROUTES) | {"link_account_conference", "add_exhibitors"}


def _coerce_input(raw):
    """Be tolerant of how Oya hands us the call. Accept a JSON object with an
    'action' key, a double-encoded JSON string, or a wrapper field
    (request/input/query/args/...) that itself contains the object or a JSON
    string. As a last resort, treat a freeform string whose first token is a
    known action (e.g. 'list_conferences IMEX America') as action + free text."""
    try:
        inp = json.loads(raw) if raw else {}
    except Exception:
        inp = raw  # not JSON — a bare string
    # Double-encoded JSON string -> parse again.
    if isinstance(inp, str):
        try:
            parsed = json.loads(inp)
            if isinstance(parsed, dict):
                inp = parsed
        except Exception:
            pass
    # Unwrap a generic wrapper field that holds the real payload.
    if isinstance(inp, dict) and "action" not in inp:
        for wrap in ("request", "input", "query", "args", "arguments", "params", "payload"):
            v = inp.get(wrap)
            if isinstance(v, dict) and "action" in v:
                return v
            if isinstance(v, str):
                try:
                    p = json.loads(v)
                    if isinstance(p, dict) and "action" in p:
                        return p
                except Exception:
                    pass
                inp = {"_raw": v}  # remember the freeform text for the fallback
                break
    # Freeform string: "<action> <rest>" where <action> is recognized.
    raw_text = inp if isinstance(inp, str) else (inp.get("_raw") if isinstance(inp, dict) else None)
    if isinstance(inp, dict) and "action" in inp:
        return inp
    if isinstance(raw_text, str):
        toks = raw_text.strip().split(None, 1)
        if toks and toks[0] in VALID_ACTIONS:
            out = {"action": toks[0]}
            if len(toks) > 1:
                # reads use q; writes won't hit this path in practice
                out["q"] = toks[1].strip()
            return out
    return inp if isinstance(inp, dict) else {}


def main():
    inp = _coerce_input(os.environ.get("INPUT_JSON", "{}"))
    base = os.environ.get("SHOWIO_BASE_URL", "https://app.tryshow.io").rstrip("/")
    key = os.environ.get("SHOWIO_API_KEY", "")
    if not key:
        print(json.dumps({"error": "SHOWIO_API_KEY not set"}))
        return

    action = inp.get("action")
    if action not in VALID_ACTIONS:
        print(json.dumps({
            "error": "Missing or invalid 'action'. Call this skill with a JSON object that "
                     "includes an 'action' key, e.g. {\"action\":\"list_conferences\",\"q\":\"fintech\"}.",
            "valid_actions": sorted(VALID_ACTIONS),
            "received": action,
        }))
        return
    args = {k: v for k, v in inp.items() if k != "action"}

    # Actions with a dynamic path segment (an id):
    if action == "link_account_conference":
        account_id = args.pop("account_id", "")
        if not account_id:
            print(json.dumps({"error": "account_id is required for link_account_conference"}))
            return
        method, path = "POST", f"/api/agent/crm/accounts/{account_id}/conference"
    elif action == "add_exhibitors":
        conference_id = args.pop("conference_id", "")
        if not conference_id:
            print(json.dumps({"error": "conference_id is required for add_exhibitors"}))
            return
        method, path = "POST", f"/api/agent/crm/conferences/{conference_id}/exhibitors"
    else:
        method, path = ROUTES.get(action, ROUTES["upsert_lead"])

    headers = {"Authorization": "Bearer " + key}
    url = base + path
    data = None

    if method == "GET":
        query = {k: v for k, v in args.items() if v not in (None, "")}
        if query:
            url += "?" + urllib.parse.urlencode(query)
    else:
        headers["Content-Type"] = "application/json"
        data = json.dumps(args).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode("utf-8"), "status": e.code}))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"error": str(e)}))


main()
