# -*- coding: utf-8 -*-
"""
EC2 Instance
"""

# Import Python libs
import boto3


__func_alias__ = {"list_": "list"}

# TODO Do this in a contract
# Can I do a soft implement of a contract, where the main definition is global,
# but it's implementation comes from a sub contract
CAMEL_MAP = {
    "availability_zone": "AvailabilityZone",
    "instance_ids": "InstanceIds",
    "dry_run": "DryRun",
    "tag_specifications": "TagSpecifications",
    "resource_type": "ResourceType",  # For tag
    "tags": "Tags",  # for tag
    "filters": "Filters",
    "multi_attach_enabled": "MultiAttachEnabled",
}


# TODO add a filter argument
async def list_(hub, ctx, filters = None, **kwargs):
    """lists instances. The kwargs can contain snake_cased versions of
    the ec2 instances collection arguments, e.g. Instances, Filters,
    etc. provided by the filter() method (see:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.PlacementGroup.instances
    which doesn't document the list of filters. Those are found here:
    https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html)

    idem exec --acct-profile=<acct profile name> aws.ec2.instance.list be_verbose=True filters='[{"Name": "tag:Name", "Values": ["<the tag you want to match>"]}

    or for a single instance based on ID:
    idem exec --acct-profile=<account profile name> aws.ec2.instance.list instance_ids='[i-081c891634d9562f8]'
    """
    ec2_res = ctx["acct"]["session"].resource("ec2")

    # TODO do this in contracts
    camelized_args = await hub.exec.aws.utils.util.camelize(CAMEL_MAP, kwargs)
    resources = ec2_res.instances.filter(**camelized_args)

    # TODO store this option in OPTS
    # TODO options for filtering output?
    # TODO automatically tag everything created with the state name?
    # TODO Keep an underlying state file to keep track of what's been created?
    # TODO Have the option of storing that state in git, or s3, or wherever
    # TODO can those logs be encrypted?
    # TODO keyvault plugin for acct for credential storage?
    # - Get azurerm credentials from aws-keyvault somehow?
    # - how do we define this in acct yaml?
    # - populate keyvault acct information as it is referenced
    if kwargs.get("be_verbose"):
        return [
            await hub.exec.aws.utils.util.bare_resource_description(item)
            for item in resources
        ]
    return [r for r in resources]


async def get(hub, ctx, instance_id=None, name=None, **kwargs):
    """use list and filtering for a single name or instance ID.

    There is a complication in the naming, where a id may refer to the
    idem equivalent of a minion's ID in the future, which is better if
    it matches the Name tag, but which... which may not exactly match
    the name tag.

    XXX: impose a convention on naming of resources, ids etc. here?
    """
    if not name and not instance_id:
        hub.log.error('Either name (the tag "Name") or instance ID must be provided.')
        return {}
    if instance_id:
        return [
            {
                instance_id: await list_(
                    hub=hub, ctx=ctx, instance_ids=[instance_id], **kwargs
                )
            }
        ]
    elif name:
        return [
            {
                name: await list_(
                    hub=hub,
                    ctx=ctx,
                    filters=[{"Name": "tag:Name", "Values": [name]}],
                    **kwargs,
                )
            }
        ]
