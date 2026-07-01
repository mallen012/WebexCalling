---
name: add-customer
description: Scaffold a new Webex Control Hub customer in this repo. Use when onboarding a new customer or when a ticket/email references a customer that has no folder yet. Creates Customers/<Name>/ from the template, and optionally creates the matching Zoho Desk account and CRM record.
---

# add-customer

Create the single source of truth for a new customer.

## Input
- Customer name (PascalCase for the folder, e.g. `HigherGround`; display name may contain
  spaces, e.g. "Higher Ground").

## Steps

1. **Check for duplicates** — look for an existing `Customers/<Name>/` and run
   `mcp__Zoho_Desk__searchAccounts` (org `875211146`) so we don't create a second record.
2. **Scaffold the folder:**
   - `Customers/<Name>/README.md` — from `templates/customer-README.md`, name filled in.
   - `Customers/<Name>/controlhub.md` — Control Hub org/site, licenses, key contacts, phone
     platform (fill what's known, leave TODOs otherwise).
   - `Customers/<Name>/tickets/` — with a `.gitkeep`.
3. **(Optional) Zoho Desk account** — if the customer isn't already a Desk account, offer to
   create one. Record the returned `accountId` in `controlhub.md`.
4. **(Optional) CRM record** — offer to create/link a CRM account via `mcp__ZohoMCP__*`.
5. **Report** the created paths and any Desk/CRM ids.

## Conventions
- Folder name: PascalCase, no spaces. Store the display name inside `README.md`.
- Always record the Zoho Desk `accountId` in `controlhub.md` once known — the
  `email-to-desk-ticket` skill uses it to link tickets to the right account.
