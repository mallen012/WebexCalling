# Kick-off prompt for the Perdigon Duo project

Create a `Perdigon` project folder on your PC, copy this `duo-push-auth`
folder into it (or clone this repo), open Claude Code in that folder, and
paste the prompt below.

---

I manage Duo MFA for the perdigon-group.com Duo account. This folder
contains `duo_user_auth.py`, a helper that talks to the Duo Admin API
(https://duo.com/docs/adminapi) using the `duo_client` Python library, with
credentials in a `.env` file (DUO_IKEY, DUO_SKEY, DUO_API_HOST — already
created from an Admin API application with read + write resource grants).

Background: my user (mike.allen) was getting passcode-only prompts because
he had no activated Duo Mobile smartphone, while luke.allen got Duo Push.
Push is offered automatically once a user has an activated smartphone, and
allowed authentication methods can also be restricted by policy per
application or per user group (precedence: app+group > app > group >
global).

Help me with the following, one step at a time, showing me each command's
output before moving on:

1. Set up the Python environment (`python -m venv`, install
   requirements.txt) and verify the API credentials work with a read-only
   call.
2. Run `compare mike.allen luke.allen` and explain any differences in their
   devices and push capability.
3. If my account isn't push-capable, walk me through `enable-push` and
   activating Duo Mobile on my phone.
4. Audit the whole account: list every active user who has NO activated
   push-capable smartphone (extend the script with an `audit` command that
   pages through all users), so I can see who else is stuck on passcodes.
5. Dump the policy summary (`policies` command) and tell me, per
   application, which authentication methods are allowed and whether any
   policy would still block Duo Push for specific sites or groups.
6. Recommend (but don't change anything without asking me) any policy
   cleanups so users get consistent push prompts across sites.

Never print or commit the contents of `.env`. Ask me before any API call
that writes or changes anything in Duo.
