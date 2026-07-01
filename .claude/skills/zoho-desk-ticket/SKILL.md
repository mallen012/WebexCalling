---
name: zoho-desk-ticket
description: General Zoho Desk ticket helpers for a customer — create, update, search, triage, and reply to support tickets. Use for direct ticket operations that aren't driven by an inbound email (for that, use email-to-desk-ticket).
---

# zoho-desk-ticket

Direct Zoho Desk ticket operations, scoped to the Perdigon Support desk.

## Account facts
- `orgId 875211146` (Perdigon Group, LLC)
- `departmentId 1075837000000006907` (Support)

## Common operations
- **List / triage:** `mcp__Zoho_Desk__getTickets` (org + dept, filter by status, assignee,
  `receivedInDays`) → summarize open work for a customer.
- **Look up a customer's tickets:** `mcp__Zoho_Desk__searchAccounts` →
  `mcp__Zoho_Desk__getTicketsByContact` / filter tickets by account.
- **Create:** `mcp__Zoho_Desk__createTicket` (link `accountId`/`contactId` when known).
- **Update:** `mcp__Zoho_Desk__updateTicket` (status, priority, assignee, due date).
- **Reply:** `mcp__Zoho_Desk__sendReply` — draft the reply and confirm before sending.
- **History / resolution:** `mcp__Zoho_Desk__getTicketHistory`,
  `mcp__Zoho_Desk__getTicketResolution`.

## Conventions
- Confirm before any create / update / reply (outward-facing).
- After creating or materially updating a ticket, mirror it into
  `Customers/<Name>/tickets/`.
