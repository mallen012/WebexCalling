#!/usr/bin/env python3
"""Duo Admin API helper for Perdigon Group.

Diagnose why a user gets passcode prompts instead of Duo Push, compare two
users' authentication setups, and enable Push by attaching and activating a
Duo Mobile smartphone.

Credentials come from environment variables (or a .env file next to this
script):

    DUO_IKEY      Admin API integration key
    DUO_SKEY      Admin API secret key
    DUO_API_HOST  api-XXXXXXXX.duosecurity.com
"""

import argparse
import json
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import duo_client


def get_admin():
    ikey = os.environ.get("DUO_IKEY")
    skey = os.environ.get("DUO_SKEY")
    host = os.environ.get("DUO_API_HOST")
    if not all([ikey, skey, host]):
        sys.exit(
            "Missing credentials: set DUO_IKEY, DUO_SKEY and DUO_API_HOST "
            "(see .env.example)."
        )
    return duo_client.Admin(ikey=ikey, skey=skey, host=host)


def find_user(admin, name):
    """Look up a Duo user by username; falls back to the email local part."""
    users = admin.get_users_by_name(name)
    if not users and "@" in name:
        users = admin.get_users_by_name(name.split("@", 1)[0])
    if not users:
        sys.exit(f"No Duo user found matching '{name}'.")
    return users[0]


def phone_push_capable(phone):
    return bool(phone.get("activated")) and "push" in (phone.get("capabilities") or [])


def user_auth_summary(admin, user):
    uid = user["user_id"]
    phones = admin.get_user_phones(uid)
    tokens = admin.get_user_tokens(uid)
    return {
        "username": user.get("username"),
        "email": user.get("email"),
        "status": user.get("status"),
        "groups": [g.get("name") for g in user.get("groups", [])],
        "phones": phones,
        "tokens": tokens,
        "push_capable": any(phone_push_capable(p) for p in phones),
    }


def print_user(summary):
    print(f"User:    {summary['username']}  <{summary['email']}>")
    print(f"Status:  {summary['status']}")
    print(f"Groups:  {', '.join(summary['groups']) or '(none)'}")
    if not summary["phones"]:
        print("Phones:  (none attached)")
    for p in summary["phones"]:
        caps = ",".join(p.get("capabilities") or [])
        act = "activated" if p.get("activated") else "NOT ACTIVATED"
        print(
            f"Phone:   {p.get('number') or '(no number)'}  "
            f"{p.get('platform') or '?'}  [{act}]  capabilities: {caps or '(none)'}"
        )
    for t in summary["tokens"]:
        print(f"Token:   {t.get('type')} serial {t.get('serial')}")
    if summary["push_capable"]:
        print("=> Duo Push IS available for this user.")
    else:
        print(
            "=> Duo Push is NOT available: no activated Duo Mobile smartphone.\n"
            "   Duo will fall back to passcodes. Run:  enable-push "
            f"{summary['username']}"
        )


def cmd_show(admin, args):
    user = find_user(admin, args.user)
    print_user(user_auth_summary(admin, user))


def cmd_compare(admin, args):
    for name in (args.user_a, args.user_b):
        user = find_user(admin, name)
        print_user(user_auth_summary(admin, user))
        print("-" * 60)
    print(
        "If one user is push-capable and the other is not, the fix is device\n"
        "activation (enable-push), not policy. If both are push-capable but\n"
        "one still gets passcode prompts on a specific site, compare the\n"
        "policies attached to that application (see the 'policies' command)."
    )


def cmd_enable_push(admin, args):
    user = find_user(admin, args.user)
    uid = user["user_id"]

    if args.sms and not args.number:
        sys.exit("--sms requires --number (the phone must be reachable by SMS).")

    phone = admin.add_phone(
        number=args.number or None, type="mobile", platform=args.platform
    )
    phone_id = phone["phone_id"]
    admin.add_user_phone(uid, phone_id)
    print(f"Attached new phone {phone_id} to {user['username']}.")

    if args.sms:
        admin.send_sms_activation_to_phone(phone_id, install="1")
        print(f"Activation link sent by SMS to {args.number}.")
    else:
        act = admin.create_activation_url(phone_id, valid_secs=86400, install="1")
        print("Open this on the phone within 24h to activate Duo Mobile:")
        print(f"  activation:   {act.get('activation_url')}")
        if act.get("installation_url"):
            print(f"  install app:  {act.get('installation_url')}")
    print(
        "Once activated, the login prompt will offer Duo Push automatically\n"
        "(assuming the application's policy allows Duo Push)."
    )


def cmd_policies(admin, args):
    resp = admin.json_api_call("GET", "/admin/v2/policies/summary", {})
    print(json.dumps(resp, indent=2, sort_keys=True))
    print(
        "\nReview each policy's authentication_methods section; a policy on an\n"
        "application or group overrides the global policy (app+group > app >\n"
        "group > global)."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("show", help="Show a user's auth devices and push capability")
    p.add_argument("user", help="Duo username or email")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("compare", help="Compare two users' auth setups")
    p.add_argument("user_a")
    p.add_argument("user_b")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser(
        "enable-push", help="Attach a smartphone and produce an activation link"
    )
    p.add_argument("user", help="Duo username or email")
    p.add_argument("--number", help="Phone number in E.164 form, e.g. +15551234567")
    p.add_argument(
        "--platform",
        default="generic smartphone",
        help='Duo platform string (default: "generic smartphone")',
    )
    p.add_argument(
        "--sms", action="store_true", help="Send the activation link by SMS"
    )
    p.set_defaults(func=cmd_enable_push)

    p = sub.add_parser("policies", help="Dump the v2 policy summary as JSON")
    p.set_defaults(func=cmd_policies)

    args = parser.parse_args()
    args.func(get_admin(), args)


if __name__ == "__main__":
    main()
