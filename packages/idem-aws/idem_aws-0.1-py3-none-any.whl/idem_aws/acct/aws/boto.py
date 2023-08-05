import boto3
from typing import Any, Dict


# Stub that will get profile info out of
# the pop `acct` plugin.
def get_session(
    hub,
    # Salt style provider info
    id: str = None,
    key: str = None,
    token: str = None,
    location: str = None,
    profile: str = None,
    # Boto3 style provider info
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    profile_name: str = None,
    # Kwargs to add to the ctx dictionary
    **ctx,
) -> Dict[str, Any]:
    """The profile name or profile-specific
    info should be returned/returnable by the
    :auth: pop module. """
    # This will expand to permit more authentication methods,
    # e.g. other profiles set in ctx['acct']
    ctx["session"] = boto3.Session(
        aws_access_key_id=aws_access_key_id or id,
        aws_secret_access_key=aws_secret_access_key or key,
        aws_session_token=aws_session_token or token,
        region_name=region_name or location,
        profile_name=profile_name or profile,
    )
    return ctx


async def gather(hub) -> Dict[str, Any]:
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("aws.boto", {}).items():
        # Add a boto session to the ctx for exec and state modules
        # Strip any args that were used for authentication
        sub_profiles[profile] = hub.acct.aws.boto.get_session(**ctx)

    # TODO default to aws environment set up the aws awy

    # TODO spin off thread to refresh sessions
    # TODO Have room for reauthenticating credentials every so often
    # TODO check the expiration and make
    # TODO specify unique roles
    return sub_profiles
