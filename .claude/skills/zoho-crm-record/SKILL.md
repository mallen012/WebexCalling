---
name: zoho-crm-record
description: Zoho CRM helpers for a customer — search, create, and update accounts, contacts, notes, and tags. Use to keep the CRM in sync with customer work (onboarding, ticket outcomes, contact changes).
---

# zoho-crm-record

Zoho CRM record operations via `mcp__ZohoMCP__*` (and `mcp__PerdiCRM__*`).

## Common operations
- **Find a record:** `mcp__ZohoMCP__ZohoCRM_searchRecords` / `getRecords` (Accounts,
  Contacts).
- **Create:** `mcp__ZohoMCP__ZohoCRM_createRecords`.
- **Update:** `mcp__ZohoMCP__ZohoCRM_updateRecord` / `updateRecords`.
- **Notes:** attach a note summarizing a ticket outcome or onboarding step.
- **Tags:** `mcp__ZohoMCP__ZohoCRM_createTags` / `postAddTags` to label customer records.

## Conventions
- Confirm before create/update (outward-facing).
- Keep the CRM account name consistent with the `Customers/<Name>/` display name.
- When a ticket resolves, consider a CRM note capturing the resolution for account history.
