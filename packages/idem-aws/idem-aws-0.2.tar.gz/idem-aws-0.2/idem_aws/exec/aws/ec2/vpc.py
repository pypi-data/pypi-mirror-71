# -*- coding: utf-8 -*-
"""
EC2 VPC
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-vpcs
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_vpcs()
    return ret
