# -*- coding: utf-8 -*-
"""
EC2 Route
"""

__func_alias__ = {"list_tables": "list"}


async def list_tables(hub, ctx):
    """
    describe-route-tables
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_route_tables()
    return ret
