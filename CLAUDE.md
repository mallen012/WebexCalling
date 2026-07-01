# WebexCalling — Customer-Ops Playbook

This repo is the portable source of truth for managing our Webex **Control Hub**
customers and the day-to-day support work around them (ticketing, CRM, provisioning).
Everything here is versioned in Git, so opening this repo from any Claude Code session
(web, desktop, or CLI) gives you the same toolkit — that is the "from anywhere" guarantee.

The MCP **connectors** (Zoho Desk, Zoho CRM, Gmail, Calendar, Webex, n8n, GitHub) are
authenticated to the claude.ai account and follow the user automatically; they are **not**
configured in this repo. This repo holds the *know-how* (skills + this playbook) and the
*customer data*.

## Repo layout

| Path | What lives here |
|------|-----------------|
| `CLAUDE.md` | This playbook — read first. |
| `.claude/skills/` | Reusable workflows (invoke as `/<skill-name>`). |
| `templates/` | Copy-me scaffolds referenced by skills. |
| `Customers/<Name>/` | One folder per customer: `README.md`, `controlhub.md`, `tickets/`. |
| `ringtones/` | Existing Webex Calling ringtone assets (leave as-is). |

**Convention:** every customer gets a folder `Customers/<Name>/` (PascalCase, no spaces).
That folder is the single source of truth for that customer. Never file work against a
customer that has no folder — run `/add-customer` first.

## Key account facts (Zoho Desk)

- **Organization:** Perdigon Group, LLC — `orgId 875211146`
- **Department:** Support — `departmentId 1075837000000006907` (the default department)
- Portal: https://support.perdigon-group.com

Use these IDs directly in `mcp__Zoho_Desk__*` calls; don't re-discover them each session.

## Tool routing — which tool for what

| Task | Tool family |
|------|-------------|
| Support tickets (create / update / triage / reply) | `mcp__Zoho_Desk__*` |
| CRM records / accounts / contacts / notes / tags | `mcp__ZohoMCP__*` (and `mcp__PerdiCRM__*`) |
| Send / draft customer email | `mcp__Gmail__*` |
| Schedule meetings / onboarding events | `mcp__Google_Calendar__*` |
| Recurring automation (event-driven flows) | `mcp__n8n-full__*` |
| Repo / PRs / issues | `mcp__github__*` |

## Skills

- `/email-to-desk-ticket` — paste a customer email; produces a structured, engineer-ready
  Zoho Desk ticket, confirms, creates it, and mirrors a copy into the customer's folder.
- `/add-customer <Name>` — scaffold a new customer folder from the template (optionally
  create the Zoho Desk account + CRM record).
- `/zoho-desk-ticket` — general ticket create/update/search/reply helpers.
- `/zoho-crm-record` — CRM record/contact/notes helpers.

## Working conventions

- **Confirm before outward actions.** Creating a ticket, sending an email, or writing to CRM
  is outward-facing — draft it, show the user, and get a yes before firing the live tool.
- **Mirror live actions into the repo.** After creating a ticket, write a copy (id + link +
  body) into `Customers/<Name>/tickets/` so the repo reflects reality.
- **Match the customer first.** Identify the customer from the folder list and
  `mcp__Zoho_Desk__searchAccounts` before filing anything; never guess the account.
