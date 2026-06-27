---
name: showio-crm
description: >
  Read or write the Show.IO CRM. Upsert a LEAD (by email) or an ACCOUNT/company
  (by name) after researching a prospect or enriching a company; or LIST the
  conferences already tracked in the CRM (action list_conferences) to dedupe
  against known events. Leads dedupe by email and notes append (never overwrite);
  accounts dedupe by company name.
credentials:
  - SHOWIO_API_KEY
  - SHOWIO_BASE_URL
inputs:
  action: "upsert_lead | upsert_account | list_conferences"
  q: "optional search text (list_conferences)"
  limit: "optional max results (list_conferences)"
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
- **list_conferences** — READ the conferences already tracked in the CRM. Call this
  first when sourcing conferences so you can SKIP ones already known and find
  competitive/complementary events around them. Returns each conference's name,
  location, region, industry, next_start_date, and website/source URL. Optional
  `q` filters by name/location/industry.
- **list_leads** — READ leads from the CRM. Pass `conference` to get the leads at
  companies exhibiting at a conference (e.g. `{"action":"list_leads","conference":"Black Hat"}`
  → the email send list for that conference, grouped by company). Optional `q`
  (name/company/email) and `limit`. Returns name, email, title, company_name,
  account_id, linkedin_url, status. Archived leads are excluded.
- **exhibitors_from_url** — extract exhibitor company names from a sponsor/exhibitor
  page URL (parses link text + image alt/title — handles many "logo wall" pages
  without a screenshot). Pass `url`. Returns `{count, names}`. Use the count to
  decide if a conference qualifies (>=30), then feed `names` into add_exhibitors.
  Example: `{"action":"exhibitors_from_url","url":"https://blackhat.com/us-26/sponsors.html"}`.
- **create_conference** — create/dedupe a conference from its URL (after checking
  `list_conferences` that it isn't already tracked). Returns the conference `id`
  (use it for add_exhibitors). Example: `{"action":"create_conference","url":"https://blackhat.com/us-26/"}`.
- **add_exhibitors** — add a list of exhibitor companies (accounts) to a conference.
  Pass `conference_id` and `exhibitors` (array of `{name, level?}`). Matches existing
  accounts (NEVER overwrites their name) or creates them, and links each to the
  conference for its year — idempotent. Example:
  `{"action":"add_exhibitors","conference_id":"<id>","exhibitors":[{"name":"Klaviyo"},{"name":"Snowflake","level":"Gold"}]}`.
  Returns `{total, created, matched, linked}`.
- **notify** — post a message to the Show.IO add-conferences Slack channel via
  Show.IO's OWN bot (NOT Oya's slack-send-message, which needs a thread_ts and
  can't post top-level). Pass `text`. Channel defaults to the add-conf channel.
  Use this to announce a qualifying conference. Example:
  `{"action":"notify","text":"✅ Added *Foo Expo 2026* (Oct 12–14, 2026) · 120 exhibitors · https://fooexpo.com — <@U…> grab a screenshot of the exhibitor wall."}`.
- **link_account_conference** — after researching where a company exhibits/sponsors,
  link the conference to its account. Pass `account_id` (from upsert_account /
  list_leads) and the conference `url`. Creates/dedupes the conference and links
  the account to it for the right year. Example:
  `{"action":"link_account_conference","account_id":"<id>","url":"https://blackhat.com/us-26/"}`.
  NOTE: `upsert_account` returns the account's currently-linked `conferences` —
  use that to decide whether research is needed (none linked, or none before 2027).

## Behavior
- Leads upsert by `email`; if a lead with that email exists, the provided fields
  are updated and `note` is appended to its note history.
- `company_name` on a lead is matched to an existing account (or a new one is
  created) and linked automatically.
- Accounts upsert by normalized company `name`.

## Examples
- `{ "action": "upsert_lead", "email": "jane@acme.com", "name": "Jane Doe", "title": "VP Sales", "company_name": "Acme", "note": "Met at ITC Vegas, interested in Q3 pilot." }`
- `{ "action": "upsert_account", "name": "Acme", "website": "acme.com", "industry": "Insurance", "revenue_range": "$50M-$100M" }`
- `{ "action": "list_conferences" }` → all tracked conferences (dedupe list)
- `{ "action": "list_conferences", "q": "insurance" }` → tracked insurance conferences
