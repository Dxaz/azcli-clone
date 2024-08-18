from knack.log import get_logger
from azure.mgmt.compute import ComputeManagementClient
from core.constants import CACHED_CREDENTIAL
from core.policies import CUSTOM_POLICIES

logger = get_logger(__name__)


def get_managment_client():
    client = ComputeManagementClient(credential=CACHED_CREDENTIAL,
                                     subscription_id='2a72a829-1f74-4dec-a113-e4b5ba752f57',
                                     policies=CUSTOM_POLICIES)
    return client

def cf_vm(client):
    client = get_managment_client().virtual_machines
    return client
