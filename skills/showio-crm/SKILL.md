---
name: showio-crm
description: >
  Create or update records in the Show.IO CRM. Use to upsert a LEAD (by email)
  or an ACCOUNT/company (by name) — e.g. after researching a prospect, logging a
  conversation, or enriching a company. Leads are deduped by email and notes are
  appended (never overwritten); accounts are deduped by company name.
credentials:
  - SHOWIO_API_KEY
  - SHOWIO_BASE_URL
inputs:
  action: "upsert_lead or upsert_account"
  email: "lead email (upsert key for leads)"
  name: "full name (or use first_name/last_name)"
  company_name: "company — links/creates the account"
  title: "job title"
  phone: "phone"
  linkedin_url: "LinkedIn URL"
  location: "city/region"
  status: "new | contacted | qualified | unqualified (leads only)"
  note: "a note to append to the lead's history"
  website: "company website (accounts)"
  industry: "industry (accounts)"
  revenue_range: "e.g. $10M-$50M (accounts)"
  employee_count: "e.g. 51-200 (accounts)"
---

# Show.IO CRM

Writes to the Show.IO CRM via its agent API.

## When to use
- **upsert_lead** — you have a person to add or update (a prospect, a contact you
  researched, someone you spoke with). Always pass `email` when you have it so the
  record dedupes instead of duplicating. Pass `note` to append what you learned.
- **upsert_account** — you have a company to add or enrich. Pass `name` (required)
  plus any of `website`, `industry`, `revenue_range`, `employee_count`, etc.

## Behavior
- Leads upsert by `email`; if a lead with that email exists, the provided fields
  are updated and `note` is appended to its note history.
- `company_name` on a lead is matched to an existing account (or a new one is
  created) and linked automatically.
- Accounts upsert by normalized company `name`.

## Examples
- `{ "action": "upsert_lead", "email": "jane@acme.com", "name": "Jane Doe", "title": "VP Sales", "company_name": "Acme", "note": "Met at ITC Vegas, interested in Q3 pilot." }`
- `{ "action": "upsert_account", "name": "Acme", "website": "acme.com", "industry": "Insurance", "revenue_range": "$50M-$100M" }`
