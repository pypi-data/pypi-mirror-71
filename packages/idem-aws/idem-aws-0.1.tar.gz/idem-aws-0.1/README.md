# AWS Cloud Provider for Idem

Amazon Web Services provides on-demand cloud computing platforms and APIs to individuals, companies, and governments,
on a metered pay-as-you-go basis. This provider is a [POP](https://gitlab.com/saltstack/pop/pop) plugin and an
extension of [Idem](https://gitlab.com/saltstack/pop/idem), allowing Idem users to leverage AWS functionality to enforce
the state of cloud infrastructure, applications, configurations, and more.

## INSTALLATION
The aws idem provider can be installed via pip:
`pip install idem-aws`

## INSTALLATION FOR DEVELOPMENT
1. Clone the `idem-aws` repository and install with pip:
`pip install -r requirements.txt`
2. Run `pip install -e <path to provider>` from your project's root directory

You are now fully set up to begin developing additional functionality for this provider.

## EXECUTION
After installation the AWS Idem Provider execution and state modules will be accessible to the hub.


## Notes about AWS and authenticion

See here for information about how the various AWS SDKs [perform
authentication](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)

Currently my understanding is that starting with the method of
creating a `Session` then using that session object to create further
connetion or resource objects is the easiest consistent way of
authenticating against the API because the session can be created with
either the secret key, key id, and/or token, or it can be used with a
profile. So creating a session and passing that around is how we're
going to start out.

The test being used is to create a `acct.yml` in this repo, with
profile info that references a valid AWS profile per the above API
configuration link.

E.g.

```
aws:
  my-staging-env:
    profile_name: my-staging-env
```

then encrypting that with acct:
```
$ acct acct.yml 
New encrypted file created at: acct.yml.fernet
The file was encrypted with this key:
-lqyMfBZ3wtWC3nJFirOmYWlIWoSR7GRHeUyQcgqKyg=
```

and then the environment setup to provide those credentials:

```
$ cat testing-env.sh 
export ACCT_KEY="-lqyMfBZ3wtWC3nJFirOmYWlIWoSR7GRHeUyQcgqKyg="
export ACCT_FILE="$PWD/acct.yml.fernet"
```

Once that test-env.sh file is sourced (while in the same directory as
the `acct.yml.fernet`), then execution modules can have the
appropriate profile (for acct, which provides the appropriate AWS
profile) used by passing the `--acct-profile` flag, e.g. for the above
case where the profile I'm going to test with is `my-staging-env`:

```
$ idem exec --acct-profile=my-staging-env aws.ec2.volume.list foo be_verbose=True filters='[{"Name": "tag:Name", "Values": ["frontend_staging-_20200320_096c9c3d1177fcc89-sda1"]}]'
```
for e.g.
