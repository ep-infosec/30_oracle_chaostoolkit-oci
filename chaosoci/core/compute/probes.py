# -*- coding: utf-8 -*-
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from oci.config import from_file
from oci.core import ComputeClient, ComputeManagementClient

from chaosoci import oci_client

from .common import filter_instances, get_instances, get_instance_pools

__all__ = ['count_instances', 'count_instance_pools']


def count_instances(filters: List[Dict[str, Any]], compartment_id: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """
    Return the number of instances in accordance with the given filters.

    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.Instance.html#oci.core.models.Instance

    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    client = oci_client(ComputeClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    instances = get_instances(client, compartment_id)

    if filters is not None:
        return len(filter_instances(instances, filters=filters))

    return len(instances)


def count_instance_pools(filters: List[Dict[str, Any]], compartment_id: str = None,
                         configuration: Configuration = None,
                         secrets: Secrets = None) -> int:
    """
    Return the number of instance pools in accordance with the given filters.

    Please refer to: https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/api/core/models/oci.core.models.InstancePool.html#oci.core.models.Instance

    for details on the available filters under the 'parameters' section.
    """  # noqa: E501
    compartment_id = compartment_id or from_file().get('compartment')

    if compartment_id is None:
        raise ActivityFailed('We have not been able to find a compartment,'
                             ' without one, we cannot continue.')

    client = oci_client(ComputeManagementClient, configuration, secrets,
                        skip_deserialization=False)

    filters = filters or None
    instance_pools = get_instance_pools(client, compartment_id)

    if filters is not None:
        return len(filter_instances(instance_pools, filters=filters))

    return len(instance_pools)
