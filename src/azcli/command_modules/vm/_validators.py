
def validate_vm_create_args(namespace):
    if namespace.image:
        image_reference = _parse_image_arg(namespace=namespace, image=namespace.image)
        # add to image_plan
        namespace.image = image_reference
        print(namespace.image)
    if namespace.os:
        os_disk = _setup_os_disk(namespace, os=namespace.os)


def _parse_image_arg(namespace, image):
    from azcli.command_modules.vm._alias import ALIASES
    aliases_by_os = ALIASES['outputs']['aliases']['value']
    

    for os in aliases_by_os:
        for alias in aliases_by_os[os]:
            if alias.lower() == image.lower():
                from azure.mgmt.compute.models import ImageReference
                namespace.os_type = os
                plan_details=aliases_by_os[os][alias]
                publisher = plan_details['publisher']
                offer = plan_details['offer']
                sku = plan_details['sku']
                version = plan_details['version']
                return ImageReference(publisher=publisher,offer=offer,sku=sku,version=version)

def _setup_os_disk(namespace, os):
    from azure.mgmt.compute.models import (OSDisk, 
                                           DiskCreateOptionTypes, 
                                           ManagedDiskParameters, 
                                           StorageAccountType, 
                                           DiskDeleteOptionTypes)
    creation_option = DiskCreateOptionTypes.FROM_IMAGE
    default = StorageAccountType.PREMIUM_LRS
    managed_disk = ManagedDiskParameters(id=None,storage_account_type=default,disk_encryption_set=None,security_profile=None)
    delete_option = DiskDeleteOptionTypes.DELETE
    return OSDisk(create_option=creation_option, os_type=os, managed_disk=managed_disk, delete_option=delete_option) 