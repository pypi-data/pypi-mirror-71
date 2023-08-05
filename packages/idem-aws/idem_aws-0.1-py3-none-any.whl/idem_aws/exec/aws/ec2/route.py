# -*- coding: utf-8 -*-
"""
EC2 Route
"""

# Import Python libs
import logging

# Import third party libs
try:
    import boto3

    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False


__func_alias__ = {"list_": "list"}

log = logging.getLogger(__name__)


def __virtual__(hub):
    return HAS_BOTO3


async def list_tables(hub, **kwargs):
    """
    describe-route-tables
    """
    ec2 = boto3.client("ec2")
    ret = ec2.describe_route_tables()
    return ret
