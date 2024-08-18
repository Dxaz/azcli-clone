import sys

from knack.log import get_logger

from core import get_default_cli

logger = get_logger(__name__)
exit_code = None

def cli_main(cli, args):
    return cli.invoke(args)

az_cli = get_default_cli()


exit_code = cli_main(az_cli, sys.argv[1:])
sys.exit(exit_code)
