# -*- coding: utf-8 -*-
"""
EC2 Subnet
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-subnets
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_subnets()
    return ret
