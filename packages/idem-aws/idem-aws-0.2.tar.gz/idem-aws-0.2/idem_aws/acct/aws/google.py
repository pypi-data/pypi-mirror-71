import io
import re
import sys
from dict_tools import data
from typing import Any, Dict

try:
    import aws_google_auth

    HAS_GOOGLE_AUTH = True
except ImportError:
    HAS_GOOGLE_AUTH = False


def __virtual__(hub):
    return HAS_GOOGLE_AUTH


def parse_opts(
    hub,
    role_arn: str,
    username: str = None,
    password: str = None,
    duration: int = None,
    idp_id: str = None,
    region: str = None,
    sp_id: str = None,
    resolve_aliases: bool = None,
    account: str = None,
    keyring: str = None,
    saml_assertion: str = None,
    saml_cache: bool = True,
    **ctx,
):
    args = data.NamespaceDict(
        {
            "duration": duration,
            "idp_id": idp_id,
            "region": region,
            "role_arn": role_arn,
            "sp_id": sp_id,
            "resolve_aliases": resolve_aliases,
            "username": username,
            "account": account,
            "keyring": keyring,
            "saml_assertion": saml_assertion,
            "saml_cache": saml_cache,
            "ask_role": False,
            "disable_u2f": False,
            "profile": None,
            "bg_response": True,
            "save_failure_html": False,
            "print_creds": True,
            "quiet": True,
            "log_level": "warn",
        }
    )

    config = aws_google_auth.resolve_config(args)

    print(
        "You may be prompted to verify your identity on a secondary 2FA device before this can continue"
    )

    out = io.StringIO()
    get_pass = aws_google_auth.util.Util.get_password

    if password is not None:
        aws_google_auth.util.Util.get_password = lambda *z: password
    sys.stdout = out
    aws_google_auth.process_auth(args, config)
    sys.stdout = sys.__stdout__
    if password is not None:
        aws_google_auth.util.Util.get_password = get_pass

    stripped_out = out.getvalue().strip().replace("\n", "")

    # export AWS_ACCESS_KEY_ID='FFFASDF2345' AWS_SECRET_ACCESS_KEY='mlkds3lk2j4y' AWS_SESSION_TOKEN='xxxxxx' AWS_SESSION_EXPIRATION='2020-06-11T12:00:31+0000'
    match = re.match(
        "(.*)export AWS_ACCESS_KEY_ID='([^']+)' AWS_SECRET_ACCESS_KEY='([^']+)' AWS_SESSION_TOKEN='([^']+)' AWS_SESSION_EXPIRATION='([^']+)'(.*)",
        stripped_out,
    )
    if match is None:
        raise ConnectionRefusedError("Could not connect to aws")

    hub.log.info(match.group(1))
    ctx["aws_access_key_id"] = match.group(2)
    ctx["aws_secret_access_key"] = match.group(3)
    ctx["aws_session_token"] = match.group(4)
    ctx["region_name"] = config.region
    session_expiration = match.group(5)
    hub.log.info(match.group(6))
    return ctx


async def gather(hub) -> Dict[str, Any]:
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("aws.google", {}).items():
        # TODO try to save these creds and load them from encrypted fernet tmp file until it expires
        # TODO refresh the session as needed when the token expires
        boto_creds = hub.acct.aws.google.parse_opts(**ctx)
        # Add a boto session to the ctx for exec and state modules
        # Strip any args that were used for authentication
        sub_profiles[profile] = hub.acct.aws.boto.get_session(**boto_creds)

    return sub_profiles
