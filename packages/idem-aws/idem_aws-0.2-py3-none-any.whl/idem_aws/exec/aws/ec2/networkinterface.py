# -*- coding: utf-8 -*-
"""
EC2 Network Interface
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-network-interfaces
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_network_interfaces()
    return ret
