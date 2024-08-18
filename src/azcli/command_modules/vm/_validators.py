
def validate_vm_create_args(namespace):
    if namespace.image:
        image = _parse_image_arg(namespace=namespace, image=namespace.image)
        # add to image_plan
        namespace.image = image
        print(namespace.image)

def _parse_image_arg(namespace, image):
    from azcli.command_modules.vm._alias import ALIASES
    aliases_by_os = ALIASES['outputs']['aliases']['value']
    

    for os in aliases_by_os:
        for alias in aliases_by_os[os]:
            if alias.lower() == image.lower():
                from azure.mgmt.compute.models import ImageReference
                plan_details=aliases_by_os[os][alias]
                publisher = plan_details['publisher']
                offer = plan_details['offer']
                sku = plan_details['sku']
                version = plan_details['version']
                return ImageReference(publisher=publisher,offer=offer,sku=sku,version=version)