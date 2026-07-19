import os

# One entry per account/organization your suite needs to sign in as. For a
# single-tenant app, keep just "default". For a multi-tenant app, add one
# key per org and set its <KEY>_EMAIL / <KEY>_PASSWORD pair in .env (see
# .env.example) — mirror the naming used here in uppercase.
CREDENTIALS = {
    "default": {
        "email": os.environ.get("DEFAULT_EMAIL"),
        "password": os.environ.get("DEFAULT_PASSWORD"),
    },
}


def get_credentials(account_id: str = "default") -> dict:
    try:
        return CREDENTIALS[account_id]
    except KeyError:
        raise KeyError(f"No credentials configured for account '{account_id}'")
