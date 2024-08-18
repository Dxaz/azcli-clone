def build_vm_resource(  # pylint: disable=too-many-locals, too-many-statements, too-many-branches
        cmd, name, location, tags, size, storage_profile, nics, admin_username,
        availability_set_id=None, admin_password=None, ssh_key_values=None, ssh_key_path=None,
        image_reference=None, os_disk_name=None, custom_image_os_type=None, authentication_type=None,
        os_publisher=None, os_offer=None, os_sku=None, os_version=None, os_vhd_uri=None,
        attach_os_disk=None, os_disk_size_gb=None, custom_data=None, secrets=None, license_type=None, zone=None,
        disk_info=None, boot_diagnostics_storage_uri=None, ultra_ssd_enabled=None, proximity_placement_group=None,
        computer_name=None, dedicated_host=None, priority=None, max_price=None, eviction_policy=None,
        enable_agent=None, vmss=None, os_disk_encryption_set=None, data_disk_encryption_sets=None, specialized=None,
        encryption_at_host=None, dedicated_host_group=None, enable_auto_update=None, patch_mode=None,
        enable_hotpatching=None, platform_fault_domain=None, security_type=None, enable_secure_boot=None,
        enable_vtpm=None, count=None, edge_zone=None, os_disk_delete_option=None, user_data=None,
        capacity_reservation_group=None, enable_hibernation=None, v_cpus_available=None, v_cpus_per_core=None,
        os_disk_security_encryption_type=None, os_disk_secure_vm_disk_encryption_set=None, disk_controller_type=None,
        enable_proxy_agent=None, proxy_agent_mode=None):

    os_caching = disk_info['os'].get('caching')

    def _build_os_profile():

        special_chars = '`~!@#$%^&*()=+_[]{}\\|;:\'\",<>/?'

        # _computer_name is used to avoid shadow names
        _computer_name = computer_name or ''.join(filter(lambda x: x not in special_chars, name))

        os_profile = {
            # Use name as computer_name if it's not provided. Remove special characters from name.
            'computerName': _computer_name,
            'adminUsername': admin_username
        }

        if count:
            os_profile['computerName'] = "[concat('{}', copyIndex())]".format(_computer_name)

        if admin_password:
            os_profile['adminPassword'] = "[parameters('adminPassword')]"

        if custom_data:
            os_profile['customData'] = b64encode(custom_data)

        if ssh_key_values and ssh_key_path:
            os_profile['linuxConfiguration'] = {
                'disablePasswordAuthentication': authentication_type == 'ssh',
                'ssh': {
                    'publicKeys': [
                        {
                            'keyData': ssh_key_value,
                            'path': ssh_key_path
                        } for ssh_key_value in ssh_key_values
                    ]
                }
            }

        if enable_agent is not None:
            if custom_image_os_type.lower() == 'linux':
                if 'linuxConfiguration' not in os_profile:
                    os_profile['linuxConfiguration'] = {}
                os_profile['linuxConfiguration']['provisionVMAgent'] = enable_agent
            elif custom_image_os_type.lower() == 'windows':
                if 'windowsConfiguration' not in os_profile:
                    os_profile['windowsConfiguration'] = {}
                os_profile['windowsConfiguration']['provisionVMAgent'] = enable_agent

        if secrets:
            os_profile['secrets'] = secrets

        if enable_auto_update is not None and custom_image_os_type.lower() == 'windows':
            os_profile['windowsConfiguration']['enableAutomaticUpdates'] = enable_auto_update

        # Windows patch settings
        if patch_mode is not None and custom_image_os_type.lower() == 'windows':
            if patch_mode.lower() not in ['automaticbyos', 'automaticbyplatform', 'manual']:
                raise ValidationError(
                    'Invalid value of --patch-mode for Windows VM. Valid values are AutomaticByOS, '
                    'AutomaticByPlatform, Manual.')
            os_profile['windowsConfiguration']['patchSettings'] = {
                'patchMode': patch_mode,
                'enableHotpatching': enable_hotpatching
            }

        # Linux patch settings
        if patch_mode is not None and custom_image_os_type.lower() == 'linux':
            if patch_mode.lower() not in ['automaticbyplatform', 'imagedefault']:
                raise ValidationError(
                    'Invalid value of --patch-mode for Linux VM. Valid values are AutomaticByPlatform, ImageDefault.')
            os_profile['linuxConfiguration']['patchSettings'] = {
                'patchMode': patch_mode
            }

        return os_profile

    def _build_storage_profile():

        storage_profiles = {
            'SACustomImage': {
                'osDisk': {
                    'createOption': 'fromImage',
                    'name': os_disk_name,
                    'caching': os_caching,
                    'osType': custom_image_os_type,
                    'image': {'uri': image_reference},
                    'vhd': {'uri': os_vhd_uri}
                }
            },
            'SAPirImage': {
                'osDisk': {
                    'createOption': 'fromImage',
                    'name': os_disk_name,
                    'caching': os_caching,
                    'vhd': {'uri': os_vhd_uri}
                },
                'imageReference': {
                    'publisher': os_publisher,
                    'offer': os_offer,
                    'sku': os_sku,
                    'version': os_version
                }
            },
            'SASpecializedOSDisk': {
                'osDisk': {
                    'createOption': 'attach',
                    'osType': custom_image_os_type,
                    'name': os_disk_name,
                    'vhd': {'uri': attach_os_disk}
                }
            },
            'ManagedPirImage': {
                'osDisk': {
                    'createOption': 'fromImage',
                    'name': os_disk_name,
                    'caching': os_caching,
                    'managedDisk': {
                        'storageAccountType': disk_info['os'].get('storageAccountType'),
                    }
                },
                'imageReference': {
                    'publisher': os_publisher,
                    'offer': os_offer,
                    'sku': os_sku,
                    'version': os_version
                }
            },
            'ManagedCustomImage': {
                'osDisk': {
                    'createOption': 'fromImage',
                    'name': os_disk_name,
                    'caching': os_caching,
                    'managedDisk': {
                        'storageAccountType': disk_info['os'].get('storageAccountType'),
                    }
                },
                "imageReference": {
                    'id': image_reference
                }
            },
            'ManagedSpecializedOSDisk': {
                'osDisk': {
                    'createOption': 'attach',
                    'osType': custom_image_os_type,
                    'managedDisk': {
                        'id': attach_os_disk
                    }
                }
            },
            'SharedGalleryImage': {
                "osDisk": {
                    "caching": os_caching,
                    "managedDisk": {
                        "storageAccountType": disk_info['os'].get('storageAccountType'),
                    },
                    "name": os_disk_name,
                    "createOption": "fromImage"
                },
                "imageReference": {
                    'sharedGalleryImageId': image_reference
                }
            },
            'CommunityGalleryImage': {
                "osDisk": {
                    "caching": os_caching,
                    "managedDisk": {
                        "storageAccountType": disk_info['os'].get('storageAccountType'),
                    },
                    "name": os_disk_name,
                    "createOption": "fromImage"
                },
                "imageReference": {
                    'communityGalleryImageId': image_reference
                }
            }
        }
        if os_disk_encryption_set is not None:
            storage_profiles['ManagedPirImage']['osDisk']['managedDisk']['diskEncryptionSet'] = {
                'id': os_disk_encryption_set,
            }
            storage_profiles['ManagedCustomImage']['osDisk']['managedDisk']['diskEncryptionSet'] = {
                'id': os_disk_encryption_set,
            }
            storage_profiles['SharedGalleryImage']['osDisk']['managedDisk']['diskEncryptionSet'] = {
                'id': os_disk_encryption_set,
            }
            storage_profiles['CommunityGalleryImage']['osDisk']['managedDisk']['diskEncryptionSet'] = {
                'id': os_disk_encryption_set,
            }
        if os_disk_security_encryption_type is not None:
            storage_profiles['ManagedPirImage']['osDisk']['managedDisk'].update({
                'securityProfile': {
                    'securityEncryptionType': os_disk_security_encryption_type,
                }
            })
            storage_profiles['ManagedCustomImage']['osDisk']['managedDisk'].update({
                'securityProfile': {
                    'securityEncryptionType': os_disk_security_encryption_type,
                }
            })
            storage_profiles['SharedGalleryImage']['osDisk']['managedDisk'].update({
                'securityProfile': {
                    'securityEncryptionType': os_disk_security_encryption_type,
                }
            })
            storage_profiles['CommunityGalleryImage']['osDisk']['managedDisk'].update({
                'securityProfile': {
                    'securityEncryptionType': os_disk_security_encryption_type,
                }
            })
            if os_disk_secure_vm_disk_encryption_set is not None:
                storage_profiles['ManagedPirImage']['osDisk']['managedDisk']['securityProfile'].update({
                    'diskEncryptionSet': {
                        'id': os_disk_secure_vm_disk_encryption_set
                    }
                })
                storage_profiles['ManagedCustomImage']['osDisk']['managedDisk']['securityProfile'].update({
                    'diskEncryptionSet': {
                        'id': os_disk_secure_vm_disk_encryption_set
                    }
                })
                storage_profiles['SharedGalleryImage']['osDisk']['managedDisk']['securityProfile'].update({
                    'diskEncryptionSet': {
                        'id': os_disk_secure_vm_disk_encryption_set
                    }
                })
                storage_profiles['CommunityGalleryImage']['osDisk']['managedDisk']['securityProfile'].update({
                    'diskEncryptionSet': {
                        'id': os_disk_secure_vm_disk_encryption_set
                    }
                })

        profile = storage_profiles[storage_profile.name]
        if os_disk_size_gb:
            profile['osDisk']['diskSizeGb'] = os_disk_size_gb
        if disk_info['os'].get('writeAcceleratorEnabled') is not None:
            profile['osDisk']['writeAcceleratorEnabled'] = disk_info['os']['writeAcceleratorEnabled']
        if os_disk_delete_option is not None:
            profile['osDisk']['deleteOption'] = os_disk_delete_option
        data_disks = [v for k, v in disk_info.items() if k != 'os']
        if data_disk_encryption_sets:
            if len(data_disk_encryption_sets) != len(data_disks):
                raise CLIError(
                    'usage error: Number of --data-disk-encryption-sets mismatches with number of data disks.')
            for i, data_disk in enumerate(data_disks):
                data_disk['managedDisk']['diskEncryptionSet'] = {'id': data_disk_encryption_sets[i]}
        if data_disks:
            profile['dataDisks'] = data_disks

        if disk_info['os'].get('diffDiskSettings'):
            profile['osDisk']['diffDiskSettings'] = disk_info['os']['diffDiskSettings']

        if disk_controller_type is not None:
            profile['diskControllerType'] = disk_controller_type

        return profile

    vm_properties = {'hardwareProfile': {'vmSize': size}, 'networkProfile': {'networkInterfaces': nics},
                     'storageProfile': _build_storage_profile()}

    vm_size_properties = {}
    if v_cpus_available is not None:
        vm_size_properties['vCPUsAvailable'] = v_cpus_available

    if v_cpus_per_core is not None:
        vm_size_properties['vCPUsPerCore'] = v_cpus_per_core

    if vm_size_properties:
        vm_properties['hardwareProfile']['vmSizeProperties'] = vm_size_properties

    if availability_set_id:
        vm_properties['availabilitySet'] = {'id': availability_set_id}

    # vmss is ID
    if vmss is not None:
        vm_properties['virtualMachineScaleSet'] = {'id': vmss}

    if not attach_os_disk and not specialized:
        vm_properties['osProfile'] = _build_os_profile()

    if license_type:
        vm_properties['licenseType'] = license_type

    if boot_diagnostics_storage_uri:
        vm_properties['diagnosticsProfile'] = {
            'bootDiagnostics': {
                "enabled": True,
                "storageUri": boot_diagnostics_storage_uri
            }
        }

    if any((ultra_ssd_enabled, enable_hibernation)):
        vm_properties['additionalCapabilities'] = {}
        if ultra_ssd_enabled is not None:
            vm_properties['additionalCapabilities']['ultraSSDEnabled'] = ultra_ssd_enabled

        if enable_hibernation is not None:
            vm_properties['additionalCapabilities']['hibernationEnabled'] = enable_hibernation

    if proximity_placement_group:
        vm_properties['proximityPlacementGroup'] = {'id': proximity_placement_group}

    if dedicated_host:
        vm_properties['host'] = {'id': dedicated_host}

    if dedicated_host_group:
        vm_properties['hostGroup'] = {'id': dedicated_host_group}

    if priority is not None:
        vm_properties['priority'] = priority

    if eviction_policy is not None:
        vm_properties['evictionPolicy'] = eviction_policy

    if max_price is not None:
        vm_properties['billingProfile'] = {'maxPrice': max_price}

    vm_properties['securityProfile'] = {}

    if encryption_at_host is not None:
        vm_properties['securityProfile']['encryptionAtHost'] = encryption_at_host

    proxy_agent_settings = {}
    if enable_proxy_agent is not None:
        proxy_agent_settings['enabled'] = enable_proxy_agent

    if proxy_agent_mode is not None:
        proxy_agent_settings['mode'] = proxy_agent_mode

    if proxy_agent_settings:
        vm_properties['securityProfile']['proxyAgentSettings'] = proxy_agent_settings

    # The `Standard` is used for backward compatibility to allow customers to keep their current behavior
    # after changing the default values to Trusted Launch VMs in the future.
    from ._constants import COMPATIBLE_SECURITY_TYPE_VALUE
    if security_type is not None and security_type != COMPATIBLE_SECURITY_TYPE_VALUE:
        vm_properties['securityProfile']['securityType'] = security_type

    if enable_secure_boot is not None or enable_vtpm is not None:
        vm_properties['securityProfile']['uefiSettings'] = {
            'secureBootEnabled': enable_secure_boot,
            'vTpmEnabled': enable_vtpm
        }

    # Compatibility of various API versions
    if vm_properties['securityProfile'] == {}:
        del vm_properties['securityProfile']

    if platform_fault_domain is not None:
        vm_properties['platformFaultDomain'] = platform_fault_domain

    if user_data:
        vm_properties['userData'] = b64encode(user_data)

    if capacity_reservation_group:
        vm_properties['capacityReservation'] = {
            'capacityReservationGroup': {
                'id': capacity_reservation_group
            }
        }

    vm = {
        'apiVersion': cmd.get_api_version(ResourceType.MGMT_COMPUTE, operation_group='virtual_machines'),
        'type': 'Microsoft.Compute/virtualMachines',
        'name': name,
        'location': location,
        'tags': tags,
        'dependsOn': [],
        'properties': vm_properties,
    }

    if zone:
        vm['zones'] = zone

    if count:
        vm['copy'] = {
            'name': 'vmcopy',
            'mode': 'parallel',
            'count': count
        }
        vm['name'] = "[concat('{}', copyIndex())]".format(name)

    if edge_zone:
        vm['extendedLocation'] = edge_zone

    return vm

def build_storage_account_resource(_, name, location, tags, sku, edge_zone=None):
    storage_account = {
        'type': 'Microsoft.Storage/storageAccounts',
        'name': name,
        'apiVersion': '2015-06-15',
        'location': location,
        'tags': tags,
        'dependsOn': [],
        'properties': {'accountType': sku}
    }

    if edge_zone:
        storage_account['apiVersion'] = '2021-04-01'
        storage_account['extendedLocation'] = edge_zone

    return storage_account

def build_nic_resource(_, name, location, tags, vm_name, subnet_id, private_ip_address=None,
                       nsg_id=None, public_ip_id=None, application_security_groups=None, accelerated_networking=None,
                       count=None, edge_zone=None):
    private_ip_allocation = 'Static' if private_ip_address else 'Dynamic'
    ip_config_properties = {
        'privateIPAllocationMethod': private_ip_allocation,
        'subnet': {'id': subnet_id}
    }

    if private_ip_address:
        ip_config_properties['privateIPAddress'] = private_ip_address

    if public_ip_id:
        ip_config_properties['publicIPAddress'] = {'id': public_ip_id}
        if count:
            ip_config_properties['publicIPAddress']['id'] = "[concat('{}', copyIndex())]".format(public_ip_id)

    ipconfig_name = 'ipconfig{}'.format(vm_name)
    nic_properties = {
        'ipConfigurations': [
            {
                'name': ipconfig_name,
                'properties': ip_config_properties
            }
        ]
    }
    if count:
        nic_properties['ipConfigurations'][0]['name'] = "[concat('{}', copyIndex())]".format(ipconfig_name)

    if nsg_id:
        nic_properties['networkSecurityGroup'] = {'id': nsg_id}

    api_version = '2015-06-15'
    if application_security_groups:
        asg_ids = [{'id': x['id']} for x in application_security_groups]
        nic_properties['ipConfigurations'][0]['properties']['applicationSecurityGroups'] = asg_ids
        api_version = '2017-09-01'

    if accelerated_networking is not None:
        nic_properties['enableAcceleratedNetworking'] = accelerated_networking
        api_version = '2016-09-01' if api_version < '2016-09-01' else api_version

    nic = {
        'apiVersion': api_version,
        'type': 'Microsoft.Network/networkInterfaces',
        'name': name,
        'location': location,
        'tags': tags,
        'dependsOn': [],
        'properties': nic_properties
    }

    if count:
        nic['name'] = "[concat('{}', copyIndex())]".format(name)
        nic['copy'] = {
            'name': 'niccopy',
            'mode': 'parallel',
            'count': count
        }

    if edge_zone:
        nic['extendedLocation'] = edge_zone
        nic['apiVersion'] = '2021-02-01'

    return nic

def build_nsg_resource(_, name, location, tags, nsg_rule):
    nsg = {
        'type': 'Microsoft.Network/networkSecurityGroups',
        'name': name,
        'apiVersion': '2015-06-15',
        'location': location,
        'tags': tags,
        'dependsOn': []
    }

    if nsg_rule != 'NONE':
        rule_name = 'rdp' if nsg_rule == 'RDP' else 'default-allow-ssh'
        rule_dest_port = '3389' if nsg_rule == 'RDP' else '22'

        nsg_properties = {
            'securityRules': [
                {
                    'name': rule_name,
                    'properties': {
                        'protocol': 'Tcp',
                        'sourcePortRange': '*',
                        'destinationPortRange': rule_dest_port,
                        'sourceAddressPrefix': '*',
                        'destinationAddressPrefix': '*',
                        'access': 'Allow',
                        'priority': 1000,
                        'direction': 'Inbound'
                    }
                }
            ]
        }

        nsg['properties'] = nsg_properties

    return nsg

def build_vnet_resource(_, name, location, tags, vnet_prefix=None, subnet=None,
                        subnet_prefix=None, dns_servers=None, edge_zone=None):
    vnet = {
        'name': name,
        'type': 'Microsoft.Network/virtualNetworks',
        'location': location,
        'apiVersion': '2015-06-15',
        'dependsOn': [],
        'tags': tags,
        'properties': {
            'addressSpace': {'addressPrefixes': [vnet_prefix]},
        }
    }
    if dns_servers:
        vnet['properties']['dhcpOptions'] = {
            'dnsServers': dns_servers
        }
    if subnet:
        vnet['properties']['subnets'] = [{
            'name': subnet,
            'properties': {
                'addressPrefix': subnet_prefix
            }
        }]
    if edge_zone:
        vnet['extendedLocation'] = edge_zone
        vnet['apiVersion'] = '2021-02-01'

    return vnet

def build_public_ip_resource(cmd, name, location, tags, address_allocation, dns_name, sku, zone, count=None,
                             edge_zone=None):
    public_ip_properties = {'publicIPAllocationMethod': address_allocation}

    if dns_name:
        public_ip_properties['dnsSettings'] = {'domainNameLabel': dns_name}

    public_ip = {
        'apiVersion': get_target_network_api(cmd.cli_ctx),
        'type': 'Microsoft.Network/publicIPAddresses',
        'name': name,
        'location': location,
        'tags': tags,
        'dependsOn': [],
        'properties': public_ip_properties
    }

    if count:
        public_ip['name'] = "[concat('{}', copyIndex())]".format(name)
        public_ip['copy'] = {
            'name': 'publicipcopy',
            'mode': 'parallel',
            'count': count
        }

    # when multiple zones are provided(through a x-zone scale set), we don't propagate to PIP becasue it doesn't
    # support x-zone; rather we will rely on the Standard LB to work with such scale sets
    if zone and len(zone) == 1:
        public_ip['zones'] = zone

    if sku and cmd.supported_api_version(ResourceType.MGMT_NETWORK, min_api='2017-08-01'):
        public_ip['sku'] = {'name': sku}

        # The edge zones are only built out using Standard SKU Public IPs
        if edge_zone and sku.lower() == 'standard':
            public_ip['apiVersion'] = '2021-02-01'
            public_ip['extendedLocation'] = edge_zone

    return public_ip

class StorageProfile(Enum):
    SAPirImage = 1
    SACustomImage = 2
    SASpecializedOSDisk = 3
    ManagedPirImage = 4  # this would be the main scenarios
    ManagedCustomImage = 5
    ManagedSpecializedOSDisk = 6
    SharedGalleryImage = 7
    CommunityGalleryImage = 8

def build_msi_role_assignment(vm_vmss_name, vm_vmss_resource_id, role_definition_id,
                              role_assignment_guid, identity_scope, is_vm=True):
    from msrestazure.tools import parse_resource_id
    result = parse_resource_id(identity_scope)
    if result.get('type'):  # is a resource id?
        name = '{}/Microsoft.Authorization/{}'.format(result['name'], role_assignment_guid)
        assignment_type = '{}/{}/providers/roleAssignments'.format(result['namespace'], result['type'])
    else:
        name = role_assignment_guid
        assignment_type = 'Microsoft.Authorization/roleAssignments'

    # pylint: disable=line-too-long
    msi_rp_api_version = '2019-07-01'
    return {
        'name': name,
        'type': assignment_type,
        'apiVersion': '2015-07-01',  # the minimum api-version to create the assignment
        'dependsOn': [
            'Microsoft.Compute/{}/{}'.format('virtualMachines' if is_vm else 'virtualMachineScaleSets', vm_vmss_name)
        ],
        'properties': {
            'roleDefinitionId': role_definition_id,
            'principalId': "[reference('{}', '{}', 'Full').identity.principalId]".format(
                vm_vmss_resource_id, msi_rp_api_version),
            'scope': identity_scope
        }
    }

# pylint: disable=too-many-locals, unused-argument, too-many-statements, too-many-branches, broad-except
def create_vm(cmd, vm_name, resource_group_name, image=None, size='Standard_DS1_v2', location=None, tags=None,
              no_wait=False, authentication_type=None, admin_password=None, computer_name=None,
              admin_username=None, ssh_dest_key_path=None, ssh_key_value=None, generate_ssh_keys=False,
              availability_set=None, nics=None, nsg=None, nsg_rule=None, accelerated_networking=None,
              private_ip_address=None, public_ip_address=None, public_ip_address_allocation='dynamic',
              public_ip_address_dns_name=None, public_ip_sku=None, os_disk_name=None, os_type=None,
              storage_account=None, os_caching=None, data_caching=None, storage_container_name=None, storage_sku=None,
              use_unmanaged_disk=False, attach_os_disk=None, os_disk_size_gb=None, attach_data_disks=None,
              data_disk_sizes_gb=None, disk_info=None,
              vnet_name=None, vnet_address_prefix='10.0.0.0/16', subnet=None, subnet_address_prefix='10.0.0.0/24',
              storage_profile=None, os_publisher=None, os_offer=None, os_sku=None, os_version=None,
              storage_account_type=None, vnet_type=None, nsg_type=None, public_ip_address_type=None, nic_type=None,
              validate=False, custom_data=None, secrets=None, plan_name=None, plan_product=None, plan_publisher=None,
              plan_promotion_code=None, license_type=None, assign_identity=None, identity_scope=None,
              identity_role=None, identity_role_id=None, application_security_groups=None, zone=None,
              boot_diagnostics_storage=None, ultra_ssd_enabled=None,
              ephemeral_os_disk=None, ephemeral_os_disk_placement=None,
              proximity_placement_group=None, dedicated_host=None, dedicated_host_group=None, aux_subscriptions=None,
              priority=None, max_price=None, eviction_policy=None, enable_agent=None, workspace=None, vmss=None,
              os_disk_encryption_set=None, data_disk_encryption_sets=None, specialized=None,
              encryption_at_host=None, enable_auto_update=None, patch_mode=None, ssh_key_name=None,
              enable_hotpatching=None, platform_fault_domain=None, security_type=None, enable_secure_boot=None,
              enable_vtpm=None, count=None, edge_zone=None, nic_delete_option=None, os_disk_delete_option=None,
              data_disk_delete_option=None, user_data=None, capacity_reservation_group=None, enable_hibernation=None,
              v_cpus_available=None, v_cpus_per_core=None, accept_term=None,
              disable_integrity_monitoring=None,  # Unused
              enable_integrity_monitoring=False,
              os_disk_security_encryption_type=None, os_disk_secure_vm_disk_encryption_set=None,
              disk_controller_type=None, disable_integrity_monitoring_autoupgrade=False, enable_proxy_agent=None,
              proxy_agent_mode=None, source_snapshots_or_disks=None, source_snapshots_or_disks_size_gb=None,
              source_disk_restore_point=None, source_disk_restore_point_size_gb=None):

    from azure.cli.core.commands.client_factory import get_subscription_id
    from azure.cli.core.util import random_string, hash_string
    from azure.cli.core.commands.arm import ArmTemplateBuilder
    from azure.cli.command_modules.vm._template_builder import (build_vm_resource,
                                                                build_storage_account_resource, build_nic_resource,
                                                                build_vnet_resource, build_nsg_resource,
                                                                build_public_ip_resource, StorageProfile,
                                                                build_msi_role_assignment,
                                                                build_vm_linux_log_analytics_workspace_agent,
                                                                build_vm_windows_log_analytics_workspace_agent)
    from azure.cli.command_modules.vm._vm_utils import ArmTemplateBuilder20190401
    from msrestazure.tools import resource_id, is_valid_resource_id, parse_resource_id

    # In the latest profile, the default public IP will be expected to be changed from Basic to Standard,
    # and Basic option will be removed.
    # In order to avoid breaking change which has a big impact to users,
    # we use the hint to guide users to use Standard public IP to create VM in the first stage.
    if cmd.cli_ctx.cloud.profile == 'latest':
        if public_ip_sku == "Basic":
            logger.warning(remove_basic_option_msg, "--public-ip-sku Standard")

    subscription_id = get_subscription_id(cmd.cli_ctx)
    if os_disk_encryption_set is not None and not is_valid_resource_id(os_disk_encryption_set):
        os_disk_encryption_set = resource_id(
            subscription=subscription_id, resource_group=resource_group_name,
            namespace='Microsoft.Compute', type='diskEncryptionSets', name=os_disk_encryption_set)
    if os_disk_secure_vm_disk_encryption_set is not None and\
            not is_valid_resource_id(os_disk_secure_vm_disk_encryption_set):
        os_disk_secure_vm_disk_encryption_set = resource_id(
            subscription=subscription_id, resource_group=resource_group_name,
            namespace='Microsoft.Compute', type='diskEncryptionSets', name=os_disk_secure_vm_disk_encryption_set)

    if data_disk_encryption_sets is None:
        data_disk_encryption_sets = []
    for i, des in enumerate(data_disk_encryption_sets):
        if des is not None and not is_valid_resource_id(des):
            data_disk_encryption_sets[i] = resource_id(
                subscription=subscription_id, resource_group=resource_group_name,
                namespace='Microsoft.Compute', type='diskEncryptionSets', name=des)

    storage_sku = disk_info['os'].get('storageAccountType')

    network_id_template = resource_id(
        subscription=subscription_id, resource_group=resource_group_name,
        namespace='Microsoft.Network')

    vm_id = resource_id(
        subscription=subscription_id, resource_group=resource_group_name,
        namespace='Microsoft.Compute', type='virtualMachines', name=vm_name)

    # determine final defaults and calculated values
    tags = tags or {}
    os_disk_name = os_disk_name or ('osdisk_{}'.format(hash_string(vm_id, length=10)) if use_unmanaged_disk else None)
    storage_container_name = storage_container_name or 'vhds'

    # Build up the ARM template
    if count is None:
        master_template = ArmTemplateBuilder()
    else:
        master_template = ArmTemplateBuilder20190401()

    vm_dependencies = []
    if storage_account_type == 'new':
        storage_account = storage_account or 'vhdstorage{}'.format(
            hash_string(vm_id, length=14, force_lower=True))
        vm_dependencies.append('Microsoft.Storage/storageAccounts/{}'.format(storage_account))
        master_template.add_resource(build_storage_account_resource(cmd, storage_account, location,
                                                                    tags, storage_sku, edge_zone))

    nic_name = None
    if nic_type == 'new':
        nic_name = '{}VMNic'.format(vm_name)
        nic_full_name = 'Microsoft.Network/networkInterfaces/{}'.format(nic_name)
        if count:
            vm_dependencies.extend([nic_full_name + str(i) for i in range(count)])
        else:
            vm_dependencies.append(nic_full_name)

        nic_dependencies = []
        if vnet_type == 'new':
            subnet = subnet or '{}Subnet'.format(vm_name)
            vnet_exists = False
            if vnet_name:
                from azure.cli.command_modules.vm._vm_utils import check_existence
                vnet_exists = \
                    check_existence(cmd.cli_ctx, vnet_name, resource_group_name, 'Microsoft.Network', 'virtualNetworks')
                if vnet_exists:
                    SubnetCreate = import_aaz_by_profile(cmd.cli_ctx.cloud.profile, "network.vnet.subnet").Create
                    try:
                        poller = SubnetCreate(cli_ctx=cmd.cli_ctx)(command_args={
                            'name': subnet,
                            'vnet_name': vnet_name,
                            'resource_group': resource_group_name,
                            'address_prefixes': [subnet_address_prefix],
                            'address_prefix': subnet_address_prefix
                        })
                        LongRunningOperation(cmd.cli_ctx)(poller)
                    except Exception:
                        raise CLIError('Subnet({}) does not exist, but failed to create a new subnet with address '
                                       'prefix {}. It may be caused by name or address prefix conflict. Please specify '
                                       'an appropriate subnet name with --subnet or a valid address prefix value with '
                                       '--subnet-address-prefix.'.format(subnet, subnet_address_prefix))
            if not vnet_exists:
                vnet_name = vnet_name or '{}VNET'.format(vm_name)
                nic_dependencies.append('Microsoft.Network/virtualNetworks/{}'.format(vnet_name))
                master_template.add_resource(build_vnet_resource(cmd, vnet_name, location, tags, vnet_address_prefix,
                                                                 subnet, subnet_address_prefix, edge_zone=edge_zone))

        if nsg_type == 'new':
            if nsg_rule is None:
                nsg_rule = 'RDP' if os_type.lower() == 'windows' else 'SSH'
            nsg = nsg or '{}NSG'.format(vm_name)
            nic_dependencies.append('Microsoft.Network/networkSecurityGroups/{}'.format(nsg))
            master_template.add_resource(build_nsg_resource(cmd, nsg, location, tags, nsg_rule))

        if public_ip_address_type == 'new':
            public_ip_address = public_ip_address or '{}PublicIP'.format(vm_name)
            public_ip_address_full_name = 'Microsoft.Network/publicIpAddresses/{}'.format(public_ip_address)
            if count:
                nic_dependencies.extend([public_ip_address_full_name + str(i) for i in range(count)])
            else:
                nic_dependencies.append(public_ip_address_full_name)
            master_template.add_resource(build_public_ip_resource(cmd, public_ip_address, location, tags,
                                                                  public_ip_address_allocation,
                                                                  public_ip_address_dns_name,
                                                                  public_ip_sku, zone, count, edge_zone))

        subnet_id = subnet if is_valid_resource_id(subnet) else \
            '{}/virtualNetworks/{}/subnets/{}'.format(network_id_template, vnet_name, subnet)

        nsg_id = None
        if nsg:
            nsg_id = nsg if is_valid_resource_id(nsg) else \
                '{}/networkSecurityGroups/{}'.format(network_id_template, nsg)

        public_ip_address_id = None
        if public_ip_address:
            public_ip_address_id = public_ip_address if is_valid_resource_id(public_ip_address) \
                else '{}/publicIPAddresses/{}'.format(network_id_template, public_ip_address)

        nics_id = '{}/networkInterfaces/{}'.format(network_id_template, nic_name)

        if count:
            nics = [
                {
                    'id': "[concat('{}', copyIndex())]".format(nics_id),
                    'properties': {
                        'deleteOption': nic_delete_option
                    }
                }
            ]
        else:
            nics = [
                {
                    'id': nics_id,
                    'properties': {
                        'deleteOption': nic_delete_option
                    }
                }
            ]

        nic_resource = build_nic_resource(
            cmd, nic_name, location, tags, vm_name, subnet_id, private_ip_address, nsg_id,
            public_ip_address_id, application_security_groups, accelerated_networking=accelerated_networking,
            count=count, edge_zone=edge_zone)
        nic_resource['dependsOn'] = nic_dependencies
        master_template.add_resource(nic_resource)
    else:
        # Using an existing NIC
        invalid_parameters = [nsg, public_ip_address, subnet, vnet_name, application_security_groups]
        if any(invalid_parameters):
            raise CLIError('When specifying an existing NIC, do not specify NSG, '
                           'public IP, ASGs, VNet or subnet.')
        if accelerated_networking is not None:
            logger.warning('When specifying an existing NIC, do not specify accelerated networking. '
                           'Ignore --accelerated-networking now. '
                           'This will trigger an error instead of a warning in future releases.')

    os_vhd_uri = None
    if storage_profile in [StorageProfile.SACustomImage, StorageProfile.SAPirImage]:
        storage_account_name = storage_account.rsplit('/', 1)
        storage_account_name = storage_account_name[1] if \
            len(storage_account_name) > 1 else storage_account_name[0]
        os_vhd_uri = 'https://{}.blob.{}/{}/{}.vhd'.format(
            storage_account_name, cmd.cli_ctx.cloud.suffixes.storage_endpoint, storage_container_name, os_disk_name)
    elif storage_profile == StorageProfile.SASpecializedOSDisk:
        os_vhd_uri = attach_os_disk
        os_disk_name = attach_os_disk.rsplit('/', 1)[1][:-4]

    if custom_data:
        custom_data = read_content_if_is_file(custom_data)

    if user_data:
        user_data = read_content_if_is_file(user_data)

    if secrets:
        secrets = _merge_secrets([validate_file_or_dict(secret) for secret in secrets])

    vm_resource = build_vm_resource(
        cmd=cmd, name=vm_name, location=location, tags=tags, size=size, storage_profile=storage_profile, nics=nics,
        admin_username=admin_username, availability_set_id=availability_set, admin_password=admin_password,
        ssh_key_values=ssh_key_value, ssh_key_path=ssh_dest_key_path, image_reference=image,
        os_disk_name=os_disk_name, custom_image_os_type=os_type, authentication_type=authentication_type,
        os_publisher=os_publisher, os_offer=os_offer, os_sku=os_sku, os_version=os_version, os_vhd_uri=os_vhd_uri,
        attach_os_disk=attach_os_disk, os_disk_size_gb=os_disk_size_gb, custom_data=custom_data, secrets=secrets,
        license_type=license_type, zone=zone, disk_info=disk_info,
        boot_diagnostics_storage_uri=boot_diagnostics_storage, ultra_ssd_enabled=ultra_ssd_enabled,
        proximity_placement_group=proximity_placement_group, computer_name=computer_name,
        dedicated_host=dedicated_host, priority=priority, max_price=max_price, eviction_policy=eviction_policy,
        enable_agent=enable_agent, vmss=vmss, os_disk_encryption_set=os_disk_encryption_set,
        data_disk_encryption_sets=data_disk_encryption_sets, specialized=specialized,
        encryption_at_host=encryption_at_host, dedicated_host_group=dedicated_host_group,
        enable_auto_update=enable_auto_update, patch_mode=patch_mode, enable_hotpatching=enable_hotpatching,
        platform_fault_domain=platform_fault_domain, security_type=security_type, enable_secure_boot=enable_secure_boot,
        enable_vtpm=enable_vtpm, count=count, edge_zone=edge_zone, os_disk_delete_option=os_disk_delete_option,
        user_data=user_data, capacity_reservation_group=capacity_reservation_group,
        enable_hibernation=enable_hibernation, v_cpus_available=v_cpus_available, v_cpus_per_core=v_cpus_per_core,
        os_disk_security_encryption_type=os_disk_security_encryption_type,
        os_disk_secure_vm_disk_encryption_set=os_disk_secure_vm_disk_encryption_set,
        disk_controller_type=disk_controller_type, enable_proxy_agent=enable_proxy_agent,
        proxy_agent_mode=proxy_agent_mode)

    vm_resource['dependsOn'] = vm_dependencies

    if plan_name:
        vm_resource['plan'] = {
            'name': plan_name,
            'publisher': plan_publisher,
            'product': plan_product,
            'promotionCode': plan_promotion_code
        }

    enable_local_identity = None
    if assign_identity is not None:
        vm_resource['identity'], _, _, enable_local_identity = _build_identities_info(assign_identity)
        role_assignment_guid = None
        if identity_scope:
            role_assignment_guid = str(_gen_guid())
            master_template.add_resource(build_msi_role_assignment(vm_name, vm_id, identity_role_id,
                                                                   role_assignment_guid, identity_scope))

    if workspace is not None:
        workspace_id = _prepare_workspace(cmd, resource_group_name, workspace)
        master_template.add_secure_parameter('workspaceId', workspace_id)
        if os_type.lower() == 'linux':
            vm_mmaExtension_resource = build_vm_linux_log_analytics_workspace_agent(cmd, vm_name, location)
            master_template.add_resource(vm_mmaExtension_resource)
        elif os_type.lower() == 'windows':
            vm_mmaExtension_resource = build_vm_windows_log_analytics_workspace_agent(cmd, vm_name, location)
            master_template.add_resource(vm_mmaExtension_resource)
        else:
            logger.warning("Unsupported OS type. Skip the connection step for log analytics workspace.")

    master_template.add_resource(vm_resource)

    if admin_password:
        master_template.add_secure_parameter('adminPassword', admin_password)

    template = master_template.build()
    parameters = master_template.build_parameters()

    # deploy ARM template
    deployment_name = 'vm_deploy_' + random_string(32)
    client = get_mgmt_service_client(cmd.cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                     aux_subscriptions=aux_subscriptions).deployments
    DeploymentProperties = cmd.get_models('DeploymentProperties', resource_type=ResourceType.MGMT_RESOURCE_RESOURCES)
    properties = DeploymentProperties(template=template, parameters=parameters, mode='incremental')
    Deployment = cmd.get_models('Deployment', resource_type=ResourceType.MGMT_RESOURCE_RESOURCES)
    deployment = Deployment(properties=properties)

    if validate:
        from azure.cli.command_modules.vm._vm_utils import log_pprint_template
        log_pprint_template(template)
        log_pprint_template(parameters)

        if cmd.supported_api_version(min_api='2019-10-01', resource_type=ResourceType.MGMT_RESOURCE_RESOURCES):
            validation_poller = client.begin_validate(resource_group_name, deployment_name, deployment)
            return LongRunningOperation(cmd.cli_ctx)(validation_poller)

        return client.validate(resource_group_name, deployment_name, deployment)

    # creates the VM deployment
    if no_wait:
        return sdk_no_wait(no_wait, client.begin_create_or_update, resource_group_name, deployment_name, deployment)
    LongRunningOperation(cmd.cli_ctx)(client.begin_create_or_update(resource_group_name, deployment_name, deployment))

    # Guest Attestation Extension and enable System Assigned MSI by default
    is_trusted_launch = security_type and security_type.lower() == 'trustedlaunch' and\
        enable_vtpm and enable_secure_boot
    if is_trusted_launch and enable_integrity_monitoring:
        vm = get_vm(cmd, resource_group_name, vm_name, 'instanceView')
        client = _compute_client_factory(cmd.cli_ctx)
        if vm.storage_profile.os_disk.os_type == 'Linux':
            publisher = 'Microsoft.Azure.Security.LinuxAttestation'
        if vm.storage_profile.os_disk.os_type == 'Windows':
            publisher = 'Microsoft.Azure.Security.WindowsAttestation'
        version = _normalize_extension_version(cmd.cli_ctx, publisher, 'GuestAttestation', None, vm.location)
        VirtualMachineExtension = cmd.get_models('VirtualMachineExtension')
        ext = VirtualMachineExtension(location=vm.location,
                                      publisher=publisher,
                                      type_properties_type='GuestAttestation',
                                      protected_settings=None,
                                      type_handler_version=version,
                                      settings=None,
                                      auto_upgrade_minor_version=True,
                                      enable_automatic_upgrade=not disable_integrity_monitoring_autoupgrade)
        try:
            LongRunningOperation(cmd.cli_ctx)(client.virtual_machine_extensions.begin_create_or_update(
                resource_group_name, vm_name, 'GuestAttestation', ext))
            logger.info('Guest Attestation Extension has been successfully installed by default '
                        'when Trusted Launch configuration is met')
        except Exception as e:
            logger.error('Failed to install Guest Attestation Extension for Trusted Launch. %s', e)
    if count:
        vm_names = [vm_name + str(i) for i in range(count)]
    else:
        vm_names = [vm_name]
    vms = []
    # Use vm_name2 to avoid R1704: Redefining argument with the local name 'vm_name' (redefined-argument-from-local)
    for vm_name2 in vm_names:
        vm = get_vm_details(cmd, resource_group_name, vm_name2)
        if assign_identity is not None:
            if enable_local_identity and not identity_scope:
                _show_missing_access_warning(resource_group_name, vm_name2, 'vm')
            setattr(vm, 'identity', _construct_identity_info(identity_scope, identity_role, vm.identity.principal_id,
                                                             vm.identity.user_assigned_identities))
        vms.append(vm)

    if workspace is not None:
        workspace_name = parse_resource_id(workspace_id)['name']
        _set_data_source_for_workspace(cmd, os_type, resource_group_name, workspace_name)

    if len(vms) == 1:
        return vms[0]
    return vms

