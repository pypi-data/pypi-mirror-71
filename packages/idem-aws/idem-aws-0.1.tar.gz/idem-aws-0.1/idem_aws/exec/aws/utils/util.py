# -*- python -*-


# TODO this can be in a contract
async def bare_resource_description(hub, resource):
    """Make a boto3 resource type into a more digestable (by idem)
    resource by simplifying it into a dictionary that doesn't have
    callable or dunder attributes

    """
    desc = {
        f: getattr(resource, f)
        for f in dir(resource)
        if (not f.startswith("__") and not callable(getattr(resource, f)))
    }
    return desc


# TODO This can also be in a contract
async def camelize(hub, camel_map, args_dict):
    """Return a dictionary that can be :**:'d or merged into the arguments
    to a function - boto3's arguments are all CamelCased to go along
    with the AWS API's conventions.

    This uses the camel_map argument to change any known key in the
    args_dict, which would be snake_cased per the conventions in
    salt/idem/pop, into being their corresponding camel-cased
    equivalents.

    Unknown keys will not be present in the returned dict.  So, This
    doesn't just camelize arguments, it also filters out arguments
    that aren't present and so would break when passed into the API.

    Values of None will be filtered out since None isn't helpful when
    passing it into the API (it breaks things)

    An example map from EBS volume resources follows:
    # Map of properties that the AWS API has in camel case, vs. the
    # snake case that is provided via salt/pop/idem
    CAMEL_MAP = {
        'availability_zone': 'AvailabilityZone',
        'encrypted': 'Encrypted',
        'iops': 'Iops',
        'kms_key_id': 'KmsKeyId',
        'size': 'Size',
        'snapshot_id': 'SnapshotId',
        'volume_type': 'VolumeType',
        'dry_run': 'DryRun',
        'tag_specifications': 'TagSpecifications',
        'resource_type': 'ResourceType', # For tag
        'tags': 'Tags',  # for tag
        'filters': 'Filters',
        'multi_attach_enabled': 'MultiAttachEnabled'
    }

    """
    in_camel_args = dict()
    for key, value in args_dict.items():
        if value is None:
            continue
        camel_key = camel_map.get(key)
        if camel_key:
            in_camel_args[camel_key] = value
    return in_camel_args
