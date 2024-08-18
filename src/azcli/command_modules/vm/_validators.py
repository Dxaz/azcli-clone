
def validate_vm_create_args(namespace):
    if namespace.image:
        image = _parse_image_arg(image=namespace.image)
        # add to image_plan
        namespace.plan = 'test'
        print(namespace.image)

def _parse_image_arg(image):
    return