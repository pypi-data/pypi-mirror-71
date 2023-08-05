async def gather(hub):
    """
    https://blog.gruntwork.io/authenticating-to-aws-with-the-credentials-file-d16c0fbcbf9e
    # TODO read the credentials in ~/.aws/credentials and ~/.aws/config
    You can store your AWS Access Keys in a Credentials File which lives in ~/.aws/credentials (or %UserProfile%\.aws\credentials on Windows). Normally, the way you create this file is by installing the AWS CLI and running the aws configure command:

    $ aws configure
    AWS Access Key ID: AKIAIOSFODNN7EXAMPLE
    AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    Default region name [None]: us-west-2
    Default output format [None]: json

    AWS prompts you to enter your Access Key ID and Secret Access Key and stores them in ~/.aws/credentials:

    [default]
    aws_access_key_id=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

    It also stores the other settings you entered in ~/.aws/config:

    [default]
    region=us-west-2
    output=json
    """
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("aws.iam", {}).items():
        raise NotImplementedError("IAM authentication is not yet implemented")

    return sub_profiles
