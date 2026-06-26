# LinkedIn Messaging (Fixed)

Send and receive LinkedIn messages via the Unipile messaging API. Drop-in replacement for the catalog `linkedin-messaging` skill — identical logic but with the correct `INPUT_JSON` sandbox entry point so it does not crash on exit 1.

## Conversations
- **list_chats** — List recent LinkedIn conversations.
- **get_chat** — Get details of a specific conversation. Provide `chat_id`.

## Messages
- **read_messages** — Read messages from a conversation. Provide `chat_id` and optional `limit`.
- **send_message** — Send a LinkedIn message in an existing conversation. Provide `chat_id` and `text`.

## Outreach
- **start_chat** — Start a new LinkedIn conversation. Provide `attendees_ids` (LinkedIn user ID) and `text`.

## Credentials required
- `UNIPILE_DSN` — Unipile REST API base URL (auto-provided by LinkedIn gateway)
- `UNIPILE_API_KEY` — Unipile API key (auto-provided by LinkedIn gateway)
- `UNIPILE_ACCOUNT_ID` — Per-user Unipile account ID (auto-provided by LinkedIn gateway)
