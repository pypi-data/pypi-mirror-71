# -*- coding: utf-8 -*-
"""
EC2 Internet Gateway
"""

# Import third party libs
__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-internet-gateways
    """
    ec2 = ctx["sessioin"].client("ec2")
    ret = ec2.describe_internet_gateways()
    return ret
