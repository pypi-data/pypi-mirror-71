# -*- coding: utf-8 -*-
"""
EC2 Image
"""

# Import third party libs
__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    describe-images
    """
    ec2 = ctx["acct"]["session"].client("ec2")
    ret = ec2.describe_images()
    return ret
