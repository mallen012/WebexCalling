# Perdigon Duo Push / Auth Helper

Tools for managing Duo MFA authentication methods for `perdigon-group.com`
via the [Duo Admin API](https://duo.com/docs/adminapi).

## The problem this solves

Two users in the same Duo account behave differently at login:

- `luke.allen` gets a **Duo Push** — tap Approve, done.
- `mike.allen` gets **no push** and has to type a passcode every time.

Duo only offers the Push method when the user has an **activated Duo Mobile
smartphone** attached to their Duo user record. No activated smartphone →
Duo falls back to passcodes (SMS / hardware token / Duo Mobile passcode).
This is a per-user device issue, not (usually) a policy issue.

Policy can also block Push per application ("site") or per user group. Duo
policy precedence, highest first:

1. Application + group policy
2. Application policy
3. User-group policy
4. Global policy

So after confirming the device is activated, if Push still doesn't appear
for a specific site, check which policy applies to that application and make
sure Duo Push is in its allowed authentication methods.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your Admin API credentials
```

Create the credentials in the Duo Admin Panel: **Applications → Protect an
Application → Admin API**. You need at minimum *Grant read resource*; add
*Grant write resource* to attach/activate phones. Keep the secret key out of
git — `.env` is ignored.

## Usage

```bash
# Why does mike get passcodes while luke gets pushes?
python duo_user_auth.py compare mike.allen luke.allen

# Full detail on one user: status, groups, phones, tokens, push capability
python duo_user_auth.py show mike.allen

# Fix it: attach a smartphone and get a Duo Mobile activation link
python duo_user_auth.py enable-push mike.allen
python duo_user_auth.py enable-push mike.allen --number "+15551234567" --sms

# List policies (v2 API) to review allowed auth methods per app/group
python duo_user_auth.py policies
```

`enable-push` prints an activation URL. Open it on the phone (or use
`--sms` to text it) — it installs/activates Duo Mobile for that user. Once
the phone shows as activated with the `push` capability, logins offer
tap-to-approve automatically.

## No-code alternative

In the Duo Admin Panel: **Users → mike.allen → Phones → Add Phone →
Activate Duo Mobile** (or "Send Activation Link via SMS"). Same result,
two minutes, no API needed. This script is for doing it repeatably and for
auditing the rest of the org.
