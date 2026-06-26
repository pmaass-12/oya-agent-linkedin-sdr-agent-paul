import os
import json
import urllib.request
import urllib.error

# Oya skill: update Show.IO CRM (leads + accounts).
# Reads INPUT_JSON (the agent's call args) and credentials from the env.
#
# Credentials (set when adding the skill to an agent):
#   SHOWIO_API_KEY   – the CRM_AGENT_API_KEY value from Show.IO
#   SHOWIO_BASE_URL  – optional, defaults to https://app.tryshow.io
#
# INPUT_JSON:
#   { "action": "upsert_lead" | "upsert_account", ...fields }
#   upsert_lead fields:   email, name|first_name|last_name, company_name,
#                         title, phone, linkedin_url, location, status, note
#   upsert_account fields: name (required), website, industry, description,
#                         linkedin_url, location, revenue_range, employee_count, phone


def main():
    inp = json.loads(os.environ.get("INPUT_JSON", "{}"))
    base = os.environ.get("SHOWIO_BASE_URL", "https://app.tryshow.io").rstrip("/")
    key = os.environ.get("SHOWIO_API_KEY", "")
    if not key:
        print(json.dumps({"error": "SHOWIO_API_KEY not set"}))
        return

    action = inp.get("action", "upsert_lead")
    path = "/api/agent/crm/accounts" if action == "upsert_account" else "/api/agent/crm/leads"
    payload = {k: v for k, v in inp.items() if k != "action"}

    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.read().decode("utf-8"), "status": e.code}))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"error": str(e)}))


main()
