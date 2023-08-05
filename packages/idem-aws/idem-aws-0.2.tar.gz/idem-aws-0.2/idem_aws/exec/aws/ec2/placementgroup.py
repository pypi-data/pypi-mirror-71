# -*- coding: utf-8 -*-
"""
EC2 Placement Group
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-placement-groups
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_placement_groups()
    return ret
