# -*- coding: utf-8 -*-
"""
EC2 Key Pair
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-key-pairs
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_key_pairs()
    return ret
