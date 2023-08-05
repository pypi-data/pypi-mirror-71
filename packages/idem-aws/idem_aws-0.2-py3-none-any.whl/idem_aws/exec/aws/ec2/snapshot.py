# -*- coding: utf-8 -*-
"""
EC2 Snapshot
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-snapshots
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_snapshots()
    return ret
