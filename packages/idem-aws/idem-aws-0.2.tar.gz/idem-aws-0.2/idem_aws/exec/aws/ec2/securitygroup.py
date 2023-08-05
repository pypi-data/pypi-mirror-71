# -*- coding: utf-8 -*-
"""
EC2 Security Group
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-security-groups
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_security_groups()
    return ret
