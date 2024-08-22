"""module docstrings"""
from core.utils import long_running_operations_handler
from azure.mgmt.compute.v2024_03_01.operations import VirtualMachinesOperations


lro = object
def dummy(client: object, resource_group: str, name: str, image: str, **kwargs):
    return

def vm_begin_assess_patches(client: object, resource_group: str, name: str):
    return long_running_operations_handler(client.begin_assess_patches(resource_group, name))

# TODO: Test this, probably should create test for everything, while your at it.
def vm_begin_capture(client, resource_group,
                     name, vhd_prefix,
                     destination_container_name='vhds',
                     overwrite_vhds=True) -> lro:
    """function docstring"""
    from azure.mgmt.compute.models import VirtualMachineCaptureParameters

    parameters = VirtualMachineCaptureParameters(vhd_prefix=vhd_prefix, destination_container_name=destination_container_name,overwrite_vhds=overwrite_vhds)
    return long_running_operations_handler(client.begin_capture(resource_group, name, parameters=parameters))

def vm_begin_convert_to_managed_disks(client, resource_group, name) -> lro:
    return long_running_operations_handler(lro=client.begin_convert_to_managed_disks(resource_group, name))

def vm_begin_create(client,
                    resource_group,
                    name,
                    location=None,
                    tags=None,
                    # Plan Settings--begin
                    plan_name=None,
                    plan_publisher=None,
                    plan_offer=None,
                    plan_promotion_code=None,
                    # ---end Plan Settings
                    # Identities---begin
                    assign_identity=None,
                    # ---end Identities
                    size='Standard_B1s',
                    zones=None,
                    # Storage Profile Params ---begin
                    storage_sku='Premium_LRS',
                    image=None,
                    attach_os_disk=None,
                    os_type=None,
                    os_disk_name=None,
                    os_disk_caching=None,
                    os_disk_delete_option=None,
                    write_accelerator=None,
                    ephemeral_os_disk_enabled=None,
                    ephemeral_os_disk_placement=None,
                    os_disk_size_gb=None,
                    os_disk_encryption_set=None,
                    os_disk_security_encryption_set=None,
                    os_disk_security_encryption_type=None,
                    attach_data_disk=None,
                    data_disk_name=None,
                    data_disk_caching=None,
                    data_disk_size_gb=None,
                    data_disk_encryption_sets=None,
                    data_disk_security_encryption_set=None,
                    data_disk_security_encryption_type=None,
                    data_disk_delete_option=None,
                    disk_controller_type=None,
                    # ---end Storage Profile
                    # Additional Capabilities ---begin
                    ultra_ssd_enabled=None,
                    hibernation_enabled=None,
                    # OS Profile ---begin
                    admin_username=None,
                    admin_password=None,
                    custom_data=None,
                    provision_vm_agent=None,
                    enable_automatic_updates=None,
                    patch_mode=None,
                    enable_hotpatching=None,
                    assessment_mode=None,
                    win_reboot_setting=None,
                    bypass_platform_safety_checks_on_user_schedule=None,
                    enable_vm_agent_platform_updates=None,
                    disable_password_authentication=None,
                    ssh_key_path=None,
                    ssh_key_data=None,
                    ssh_key_name=None,
                    allow_extension_operations=None,
                    # ---end OS Profile
                    # Network Profile ---begin
                    nics=None,
                    nics_delete_option=None,
                    accelerated_networking=None,
                    disable_tcp_state_tracking=None,
                    enable_fpga=None,
                    enable_ip_forwarding=None,
                    nsg=None,
                    dns_servers=None,
                    public_ip_name=None,
                    public_ip_sku=None,
                    public_ip_tier=None,
                    public_ip_allocation_method=None,
                    application_security_groups=None,
                    load_balancer_backend_address_pools=None,
                    nic_auxiliary_mode=None,
                    nic_auxiliary_sku=None,
                    # ---end Networking Profile
                    # Security Profile ---begin
                    secure_boot_enabled=None,
                    v_tpm_enabled=None,
                    encryption_at_host=None,
                    security_type=None,
                    proxy_agent_enabled=None,
                    proxy_agent_mode=None,
                    key_incarnation_id=None,
                    # ---end Security Profile
                    # Boot Diagnostics ---begin
                    boot_diagnostics_enabled=None,
                    boot_diagnostics_storage_uri=None,
                    availability_set=None,
                    virtual_machine_scale_set=None,
                    proximity_placement_group=None,
                    priority=None,
                    eviction_policy=None,
                    spot_max_price=None,
                    host=None,
                    host_group=None,
                    license_type=None,
                    extensions_time_budget=None,
                    platform_fault_domain=None,
                    user_data=None,
                    capacity_reservation=None,
                    gallery_applications=None,
                    **kwargs) -> lro:

    from azure.mgmt.compute.models import (VirtualMachine,
                                           Plan, 
                                           VirtualMachineIdentity,
                                           UserAssignedIdentitiesValue,
                                           ResourceIdentityType,
                                           ExtendedLocation,
                                           HardwareProfile,
                                           ScheduledEventsPolicy,
                                           StorageProfile,
                                           AdditionalCapabilities,
                                           OSProfile,
                                           NetworkProfile,
                                           SecurityProfile,
                                           DiagnosticsProfile,
                                           SubResource,
                                           VirtualMachinePriorityTypes,
                                           VirtualMachineEvictionPolicyTypes,
                                           BillingProfile,
                                           ScheduledEventsProfile,
                                           CapacityReservationProfile,
                                           ApplicationProfile)
     
    parameters = VirtualMachine(location=location,
                                tags=tags,
                                plan=plan,
                                identity=identity,
                                zones=zones,
                                extended_location=None,
                                hardware_profile=hardware_profile,
                                scheduled_events_policy=None,
                                storage_profile=storage_profile,
                                additional_capabilities=additional_capabilities,
                                os_profile=os_profile,
                                network_profile=network_profile,
                                security_profile=security_profile,
                                diagnostics_profile=diagnostics_profile,
                                availability_set=availability_set,
                                virtual_machine_scale_set=virtual_machine_scale_set,
                                proximity_placement_group=proximity_placement_group,
                                priority=priority,
                                eviction_policy=eviction_policy,
                                billing_profile=billing_profile,
                                host=host,
                                host_group=host_group,
                                #license_type=license_type,
                                #extensions_time_budget=extensions_time_budget,
                                #platform_fault_domain=platform_fault_domain,
                                scheduled_events_profile=scheduled_events_profile,
                                #user_data=user_data,
                                capacity_reservation=capacity_reservation,
                                application_profile=application_profile)

    return vm_begin_create_or_update(client, resource_group, name, parameters)

def vm_begin_create_or_update(client, resource_group, name, parameters,if_match=None, if_none_match=None) -> lro:
    return long_running_operations_handler(client.begin_create_or_update(resource_group, name, parameters=parameters))

def vm_begin_deallocate(client, resource_group, name, hibernate: bool=None) -> lro:
    return long_running_operations_handler(lro=client.begin_deallocate(resource_group, name, hibernate=hibernate))

def vm_begin_delete(client, resource_group, name, force_deletion: bool=None) -> lro:
    return long_running_operations_handler(lro=client.begin_delete(resource_group, name, force_deletion=force_deletion))

def vm_begin_install_patches(client, resource_group,
                             name, maximum_duration,
                             reboot_setting, classifications_to_include_linux = None,
                             classifications_to_include_windows = None,
                             package_name_masks_to_include = None,
                             kb_numbers_to_include = None,
                             package_name_masks_to_exclude = None,
                             kb_numbers_to_exclude = None,
                             maintenance_run_id = None,
                             exclude_kbs_requiring_reboot = None,
                             max_patch_publish_date = None) -> lro:
    
    from azure.mgmt.compute.models import (LinuxParameters, 
                                           VirtualMachineInstallPatchesParameters, 
                                           WindowsParameters)

    windows_parameters = WindowsParameters(classifications_to_include = classifications_to_include_windows,
                                           kb_numbers_to_include = kb_numbers_to_include,
                                           kb_numbers_to_exclude = kb_numbers_to_exclude,
                                           exclude_kbs_requiring_reboot = exclude_kbs_requiring_reboot,
                                           max_patch_publish_date = max_patch_publish_date)

    linux_parameters = LinuxParameters(classifications_to_include = classifications_to_include_linux,
                                       package_name_masks_to_include = package_name_masks_to_include,
                                       package_name_masks_to_exclude = package_name_masks_to_exclude,
                                       maintenance_run_id = maintenance_run_id)

    install_patches_input = VirtualMachineInstallPatchesParameters(reboot_setting = reboot_setting,
                                                                    maximum_duration = maximum_duration,
                                                                    linux_parameters=linux_parameters,
                                                                    windows_parameters=windows_parameters)
    return long_running_operations_handler(lro=client.begin_install_patches(resource_group,name,install_patches_input))

def vm_begin_perform_maintenance(client, resource_group, name) -> lro:
    """https://learn.microsoft.com/en-us/azure/virtual-machines/maintenance-notifications-cli"""
    return long_running_operations_handler(lro=client.begin_perform_maintenance(resource_group, name))

def vm_begin_power_off(client, resource_group, name, skip_shutdown=False) -> lro:
    return long_running_operations_handler(client.begin_power_off(resource_group, name, skip_shutdown=skip_shutdown))

def vm_begin_reapply(client, resource_group, name) -> lro:
    return long_running_operations_handler(lro=client.begin_reapply(resource_group, name))

def vm_begin_redeploy(client, resource_group, name) -> lro:
    return long_running_operations_handler(lro=client.begin_redeploy(resource_group, name))

def vm_begin_reimage(client, resource_group, name, parameters) -> lro:
    return list()

def vm_begin_restart(client, resource_group, name) -> lro:
    return long_running_operations_handler(lro=client.begin_restart(resource_group, name))

def vm_begin_run_command(client, resource_group, name, parameters) -> lro:
    return list()

def vm_begin_start(client, resource_group, name) -> lro:
    return long_running_operations_handler(lro=client.begin_start(resource_group, name))

def vm_begin_update(client, resource_group, name) -> lro:
    """
                    tags=None,
                    plan=None,
                    identity=None,
                    zones=None,
                    extended_location=None,
                    hardware_profile=None,
                    scheduled_events_policy=None,
                    storage_profile=None,
                    additional_capabilities=None,
                    os_profile=None,
                    network_profile=None,
                    security_profile=None,
                    diagnostics_profile=None,
                    availability_set=None,
                    virtual_machine_scale_set=None,
                    proximity_placement_group=None,
                    priority=None,
                    eviction_policy=None,
                    billing_profile=None,
                    host=None,
                    host_group=None,
                    license_type=None,
                    extensions_time_budget=None,
                    platform_fault_domain: int=None,
                    scheduled_events_profile=None,
                    user_data=None,
                    capacity_reservation=None,
                    application_profile=None
    """
    return list()
    
def vm_generalize(client, resource_group, name) -> None:
    return client.generalize(resource_group_name=resource_group, name=name)

def vm_get(client, resource_group, name, expand=None):
    return client.get(resource_group,name,expand=expand)

def vm_instance_view(client, resource_group, name):
    return client.instance_view(resource_group_name=resource_group,vm_name=name)

def vm_list(client: object, resource_group: str):
     return list(client.list(resource_group_name=resource_group))

def vm_list_all(client: object, resource_group: str=None):
    if resource_group and resource_group != '':
        return vm_list(client, resource_group)
    return list(client.list_all())

def vm_list_available_sizes(client, resource_group, name):
    return list(client.list_available_sizes(resource_group, name))

def vm_list_by_location(client, location):
    return list(client.list_by_location(location))

def vm_retrieve_boot_diagnostics_data(client, resource_group, name, expiration_time_in_minutes: int=None):
    return client.retrieve_boot_diagnostics_data(resource_group, name, sas_uri_expiration_time_in_minutes=expiration_time_in_minutes)

def vm_simulate_eviction(client, resource_group, name) -> None:
    return list()
