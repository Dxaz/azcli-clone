# import sys
# sys.path.append('/commands/vm/')

from knack.cli import CLI
from knack.arguments import ArgumentsContext
from knack.commands import CLICommandsLoader, CommandGroup
from knack.log import get_logger

from core.client_factory import cf_vm
from core.constants import EXCLUDED_ARGS

logger = get_logger(__name__)


def get_config_dir():
    import os
    return os.getenv('AZURE_CONFIG_DIR', None) or os.path.expanduser(os.path.join('~', 'projects', 'azure', 'cli-clone', '.config'))

GLOBAL_CONFIG_DIR = get_config_dir()
ENV_VAR_PREFIX = 'AZURE-CLONE'

__version__ = "0.0.1"


class AzCLI(CLI):

    def __init__(self, **kwargs):
        super(AzCLI, self).__init__(**kwargs)

        config_folder = None
        
    def get_cli_version(self):
        return __version__
    
    def exception_handler(self, ex):
        """ exception handler """

        from azure.core.exceptions import ClientAuthenticationError, ResourceExistsError
        if isinstance(ex, ClientAuthenticationError):
            logger.error('No cached creds found')
            return 2
        if isinstance(ex, ResourceExistsError):
            logger.error(ex.message)
            return 1
        else:
            logger.error(ex)
        return 1


class MyCommandLoader(CLICommandsLoader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.excluded_command_handler_args = EXCLUDED_ARGS

    def load_command_table(self, args):
        with CommandGroup(self,'vm','azcli.command_modules.vm.commands#{}',client_factory=cf_vm) as g:
            g.command('assess-patches', 'vm_begin_assess_patches')
            # TODO: change this back to correct handler
            g.command('create','dummy')
            g.command('capture','vm_begin_capture')
            g.command('convert','vm_begin_convert_to_managed_disks')
            g.command('deallocate','vm_begin_deallocate')
            g.command('delete','vm_begin_delete')
            g.command('generalize','vm_generalize')
            g.command('install-patches', 'vm_begin_install_patches')
            g.command('instance-view','vm_instance_view')
            g.command('list', 'vm_list_all')
            g.command('list-by-location','vm_list_by_location')
            g.command('list-sizes','vm_list_available_sizes')
            g.command('perform-maintenance','vm_begin_perform_maintenance')
            g.command('reapply','vm_begin_reapply')
            g.command('redeploy','vm_begin_redeploy')
            g.command('restart','vm_begin_restart')
            g.command('show','vm_get')
            g.command('start','vm_begin_start')
            g.command('stop','vm_begin_power_off')
        
        with CommandGroup(self,'vm boot-diagnostics','commands.vm.commands#{}',client_factory=cf_vm) as g:
            g.command('get-boot-log-uris','vm_retrieve_boot_diagnostics_data')
            #g.command('','')
        return super().load_command_table(args)

    def load_arguments(self, command):

        from azure.mgmt.compute.v2023_03_01.models import (InstanceViewTypes,
                                                           VirtualMachineCaptureParameters, 
                                                           VirtualMachineSizeTypes,
                                                           VMGuestPatchClassificationLinux, 
                                                           VMGuestPatchClassificationWindows)
        from core.utils import get_enum_type
        from azcli.command_modules.vm._validators import validate_vm_create_args

        # TODO: get_enum_type found in /src/azure-cli-core/azure/cli/core/commands/parameters.py 
        # Figure out how that works exactly, added it to utils.py for now. I know it makes it caseinsensitive
        # due to argtype overrides but why doe? how id do dah?

        with ArgumentsContext(self, 'vm') as ac:
            ac.argument('resource_group', type=str, options_list=('--resource-group', '-g'))
            ac.argument('name', type=str, options_list=('--name', '-n'))

        with ArgumentsContext(self, 'vm create') as ac:
            ac.argument('location', options=('--location', '-l'))
            ac.argument('vm_size', arg_type=get_enum_type(VirtualMachineSizeTypes))
            ac.argument('image', validator=validate_vm_create_args)
    
        with ArgumentsContext(self, "vm boot-diagnostics get-boot-log-uris") as ac:
            ac.argument('expiration_time_in_minutes', type=int, options_list=('--expiration-time-in-minutes','-e'), default=None)

        with ArgumentsContext(self, "vm install-patches") as ac:
            ac.argument('classifications_to_include_linux', type=str, arg_type=get_enum_type(VMGuestPatchClassificationLinux), nargs='+')
            ac.argument('classifications_to_include_windows', type=str, arg_type=get_enum_type(VMGuestPatchClassificationWindows), nargs='+') #, choices=['Critical', 'Definition', 'Feature_pack', 'Security', 'Service_pack', 'Tools', 'Updates', 'update_roll_up'])
            ac.argument('package_name_masks_to_include',nargs='+')
            ac.argument('kb_numbers_to_include', type=str, nargs='+')
            ac.argument('package_name_masks_to_exclude', type=str, nargs='+')
            ac.argument('kb_numbers_to_exclude', type=str, nargs='+')
            ac.argument('exclude_kbs_requiring_reboot', type=bool)

        with ArgumentsContext(self, "vm list-by-location") as ac:
            ac.argument('location', options_list=('--location','-l'), required=True)
        
        with ArgumentsContext(self, "vm show") as ac:
            ac.argument('expand', argType=get_enum_type(InstanceViewTypes), choices=['instanceView','userData'])


        return super().load_arguments(command)

        # TODO:
        # Fix this in azure-cli-core src/azure-cli/azure/cli/command_modules/vm/custom.py
        # kb_numbers_to_inclunde
        # exclude_kbs_requirig_reboot
        # Error given: kb_numbers_to_inclunde is not a known attribute of class <class 'azure.mgmt.compute.v2024_03_01.models._models_py3.WindowsParameters'> and will be ignored
        # exclude_kbs_requirig_reboot is not a known attribute of class <class 'azure.mgmt.compute.v2024_03_01.models._models_py3.WindowsParameters'> and will be ignored
        # it went unnoticed for like 3 years lawl. 
        # Ref: https://github.com/Azure/azure-cli/pull/17549/commits/3a5091e96092fa563e985df6b0339ba6ebc6ae66

def get_default_cli():
    return AzCLI(cli_name='az-clone',
                 config_dir=GLOBAL_CONFIG_DIR,
                 config_env_var_prefix=ENV_VAR_PREFIX,
                 commands_loader_cls=MyCommandLoader
                 )