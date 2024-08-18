from os import getenv
from azure.identity import DefaultAzureCredential

ANSI_CONTROL_SEQUENCE_INITIATOR = '\x1b['
ANSI_ERASE_LINE = '%sK' % ANSI_CONTROL_SEQUENCE_INITIATOR
ANSI_HIDE_CURSOR = '%s?25l' % ANSI_CONTROL_SEQUENCE_INITIATOR
ANSI_SHOW_CURSOR = '%s?25h' % ANSI_CONTROL_SEQUENCE_INITIATOR

CACHED_CREDENTIAL = DefaultAzureCredential()
EXCLUDED_ARGS = ['self','kwargs','args','client']


# for testing
SUBSCRIPTION_ID = getenv('AZURE_SUB_ID')
