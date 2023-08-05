# -*- coding: utf-8 -*-
"""
EC2 Instance
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, **kwargs):
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
    return ec2_res.instances.filter(**kwargs)


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
