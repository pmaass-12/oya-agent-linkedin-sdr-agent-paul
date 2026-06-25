import os, json, httpx

try:
    base_url = os.environ.get("PAUL_CRM_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("PAUL_CRM_API_KEY", "")

    if not base_url:
        raise ValueError("PAUL_CRM_BASE_URL environment variable is not set.")
    if not api_key:
        raise ValueError("PAUL_CRM_API_KEY environment variable is not set.")

    inp = json.loads(os.environ.get("INPUT_JSON", "{}"))

    name = inp.get("name", "").strip()
    email = inp.get("email", "").strip()

    if not name:
        raise ValueError("'name' is required.")
    if not email:
        raise ValueError("'email' is required.")

    lead_id = inp.get("lead_id", "").strip()

    payload = {k: v for k, v in {
        "name": name,
        "email": email,
        "title": inp.get("title"),
        "company": inp.get("company"),
        "linkedin_url": inp.get("linkedin_url"),
        "source": inp.get("source"),
        "status": inp.get("status"),
        "enrichment_timestamp": inp.get("enrichment_timestamp"),
    }.items() if v is not None}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    with httpx.Client(timeout=20) as client:
        if lead_id:
            url = f"{base_url}/leads/{lead_id}"
            response = client.patch(url, json=payload, headers=headers)
        else:
            url = f"{base_url}/leads"
            response = client.post(url, json=payload, headers=headers)

        if response.status_code in (200, 201, 204):
            try:
                data = response.json()
            except Exception:
                data = {}

            crm_lead_id = (
                data.get("id")
                or data.get("lead_id")
                or data.get("data", {}).get("id")
                or lead_id
                or None
            )

            result = {
                "success": True,
                "operation": "update" if lead_id else "create",
                "lead_id": str(crm_lead_id) if crm_lead_id is not None else None,
                "status_code": response.status_code,
            }
        else:
            try:
                error_body = response.json()
            except Exception:
                error_body = response.text

            result = {
                "success": False,
                "error": f"CRM returned HTTP {response.status_code}",
                "status_code": response.status_code,
                "detail": error_body,
            }

    print(json.dumps(result))

except Exception as e:
    print(json.dumps({"error": str(e)}))