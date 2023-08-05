# -*- coding: utf-8 -*-
"""
EC2 Network ACL
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


async def list_(hub, **kwargs):
    """
    describe-network-acls
    """
    ec2 = boto3.client("ec2")
    ret = ec2.describe_network_acls()
    return ret
