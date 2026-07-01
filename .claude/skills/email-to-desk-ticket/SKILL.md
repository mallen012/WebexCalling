---
name: email-to-desk-ticket
description: Turn a pasted or forwarded customer email into a structured, engineer-ready Zoho Desk ticket. Use when a customer reports one or more issues by email and you want a ticket opened to investigate. Identifies the customer, breaks the email into discrete issues with next-steps, confirms, creates the ticket in the Perdigon Support desk, and mirrors a copy into the customer's folder.
---

# email-to-desk-ticket

Convert an inbound customer email into a Zoho Desk ticket that an engineer can act on.

## Inputs
- The email text (pasted or forwarded). Sender name/address and body.
- Optional: a specific customer name if the sender is ambiguous.

## Account facts (from CLAUDE.md)
- Zoho Desk org: `orgId 875211146` (Perdigon Group, LLC)
- Department: `departmentId 1075837000000006907` (Support)

## Steps

### 1. Identify the customer
- Scan `Customers/*/` for a matching folder (by name, contacts, or email domain).
- Cross-check with `mcp__Zoho_Desk__searchAccounts` (org `875211146`, `accountName` or
  `_all`) and `mcp__Zoho_Desk__searchContacts` on the sender's email.
- If no confident match: **stop and ask** whether to run `/add-customer` first. Never file
  a ticket against the wrong or a missing account.

### 2. Extract the issues
Split the email into discrete, numbered problems. For each, capture the customer's own
evidence: frequency (e.g. "~50%", "~15%"), affected users/devices, and what they already
ruled out (e.g. "persisted after handset swap → not hardware").

### 3. Draft the ticket
Use `templates/ticket-body.md`. Produce:
- **Subject:** `<Customer> — <short summary of primary issue(s)>`
- One **section per issue**: symptom in the customer's words → likely area →
  **investigation next-steps** phrased for a Webex Calling engineer.
- An **Environment / already ruled out** block.
- Priority suggestion based on business impact.

### 4. Confirm, then create
Show the full draft to the user. On approval, call `mcp__Zoho_Desk__createTicket`:
- `orgId: 875211146`, `departmentId: 1075837000000006907`
- `subject`, `description` (the drafted body), `contactId`/`accountId` when matched,
  `priority` and `channel: "Email"`.
Default posture is **draft + confirm**. `--auto` mode: skip the confirmation only when the
user explicitly asks (customer already matched, trusted).

### 5. Log locally
Write the created ticket to `Customers/<Name>/tickets/<ticketNumber>-<slug>.md` with the
ticket id, portal link, and the body. This keeps the repo (and the local
`deployment-cli` / `webex-aa-toolkit` projects) in sync with Desk.

## Worked example (the landline email)

Sender reports three telephony problems that persisted across a handset replacement
(→ not hardware; points at calling config / network / codec):

1. **Zoom dial-in incompatibility** — loud digital buzzing heard by the far end on
   Zoom-hosted calls and calls to Zoom virtual numbers.
   → *Next steps:* check codec negotiation (G.711 vs G.729/Opus) and DTMF/in-band audio
   handling on the Webex Calling trunk and MPP handsets; capture a sample call for media
   analysis.
2. **Conference merge fails ~50%** — pressing "Conf" doesn't merge the two legs (Anikah,
   Mark, Mark Wright).
   → *Next steps:* verify 3-way conference / local vs network conferencing config on the
   MPP devices; confirm firmware and calling license support for merge.
3. **Call drops / one-way audio ~15%** — on connect, far party is dropped or can't hear
   (Anikah, Mark Wright).
   → *Next steps:* run call-drop + one-way-audio (NAT / media-path / SBC) diagnostics;
   pull CDRs and check media routing.

Resulting subject: `<Customer> — Landline issues: Zoom buzzing, conference merge failures, call drops`
