---
name: paul-crm-lead-writer
display_name: "Paul's CRM Lead Writer"
category: sales
description: "POSTs a structured lead object to Paul's CRM endpoint or PATCHes an existing lead by ID on status/meeting updates."
icon: user-plus
skill_type: sandbox
catalog_type: addon
requirements: "httpx>=0.25"
resource_requirements:
  - env_var: PAUL_CRM_BASE_URL
    name: "Paul's CRM Base URL"
    description: "Base URL of Paul's homegrown CRM API, e.g. https://crm.example.com/api"
  - env_var: PAUL_CRM_API_KEY
    name: "Paul's CRM API Key"
    description: "Bearer token or API key for authenticating with Paul's CRM"
tool_schema:
  name: paul_crm_lead_writer
  description: "Create a new lead (POST) or update an existing lead (PATCH) in Paul's CRM. Returns the CRM-assigned lead ID on success."
  parameters:
    type: object
    properties:
      lead_id:
        type: "string"
        description: "Existing CRM lead ID. If provided, issues a PATCH/PUT to update the lead instead of creating a new one."
      name:
        type: "string"
        description: "Full name of the lead."
      title:
        type: "string"
        description: "Job title of the lead."
      company:
        type: "string"
        description: "Company the lead works at."
      email:
        type: "string"
        description: "Email address of the lead."
      linkedin_url:
        type: "string"
        description: "LinkedIn profile URL of the lead."
      source:
        type: "string"
        description: "Where the lead came from, e.g. 'LinkedIn', 'Referral', 'Conference'."
      status:
        type: "string"
        description: "Current lead status, e.g. 'new', 'contacted', 'meeting_booked', 'qualified', 'closed'."
      enrichment_timestamp:
        type: "string"
        description: "ISO 8601 timestamp of when the lead data was last enriched, e.g. '2024-06-01T12:00:00Z'."
    required: [name, email]
---
# Paul's CRM Lead Writer
Write or update a structured lead record directly to Paul's homegrown CRM via REST API.

## Be Proactive
Call this skill immediately whenever a new lead is identified, a lead's status changes (e.g. meeting booked, qualified), or enrichment data is available that should be persisted to the CRM. Do not wait for the user to ask — write the data as soon as it is ready.