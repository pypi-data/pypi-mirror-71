# npm install --global gsts
# gsts --aws-role-arn arn:aws:iam::99999999999:role/xacct/developer --aws-profile=default --sp-id 99999999 --idp-id 999999999 --username foo@example.com


async def gather(hub):
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("aws.gsts", {}).items():
        raise NotImplementedError("GSTS authentication is not yet implemented")

    return sub_profiles
