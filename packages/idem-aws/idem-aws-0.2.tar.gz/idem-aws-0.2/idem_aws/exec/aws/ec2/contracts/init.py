from typing import Any, Dict, List

# TODO Can I do a soft implement of a contract, where the main definition is global,
# TODO but it's implementation comes from a sub contract
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


def sig_list(hub, ctx, **kwargs) -> List[Dict[str, Any]]:
    """
    A contract to define the arguments acceptable to any ec2 list function
    """


def pre_list(hub, ctx):
    """
    Make sure that we have an account and a session
    """
    func_ctx = ctx.args[1]
    assert "acct" in func_ctx
    assert func_ctx["acct"].get("session")


async def call_list(hub, ctx):
    kwargs = await hub.exec.aws.init.camelize(CAMEL_MAP, ctx.kwargs)
    return await ctx.func(*ctx.args, **kwargs)


async def post_list(hub, ctx):
    resources = ctx.ret

    if hub.OPT.idem.be_verbose:
        return [
            await hub.exec.aws.init.bare_resource_description(item)
            for item in resources
        ]
    else:
        return [r for r in resources]
