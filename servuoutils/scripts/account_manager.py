import os
import sys
import signal
import argparse

import pathlib

import getpass

from servuoutils.account_manager import EncryptAlgorithm
from servuoutils.account_manager import AccessLevel
from servuoutils.account_manager import AccountManager

import structlog
logger = structlog.get_logger()

# Global variables
parser = None
args = None

ROOT_PATH = pathlib.Path().absolute()
# TODO change default value to another better
ACCOUNTS_FILE = os.path.realpath(os.path.join(ROOT_PATH, 
    "submodules", "ServUO", 
    "Saves", "Accounts", "accounts.xml"))

ENCRYPTION_TYPE = EncryptAlgorithm.NewSecureCrypt
ACCESS_TYPE = AccessLevel.Player.name

################################################################################
# Functions ####################################################################
################################################################################
def signal_handler(sig, frame):
    logger.info("Signal", sig=sig)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Helper to manage server accounts.",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-l','--list', help='List update accounts', default="", action='store_true')
    parser.add_argument('-i','--info', help='Get info from an account', default="", type=str, metavar='account_name')
    parser.add_argument('-c','--create', help='Create a game account if no exists', default="", type=str, metavar='account_name')
    parser.add_argument('-t','--type', help='Set up another encryption type. Use none, md5, NewCrypt, NewCrypt (Recommended)', default="NewSecureCrypt", type=str, metavar='path')
    parser.add_argument('-a','--access_level', help='Set up the access level of the account. Use Player (Recommended)', default="Player", type=str, metavar='access-level')
    parser.add_argument('-d','--delete', help='Delete an account if exist.', default="", type=str, metavar='account_name')
    parser.add_argument('-f','--file', help='Set up working directory', default=ACCOUNTS_FILE, type=str, metavar='path')
    
    args = parser.parse_args()

    if args.file:
        ACCOUNTS_FILE = args.file

    if not os.path.isfile(ACCOUNTS_FILE):
        logger.error("file_not_found", file=ACCOUNTS_FILE)
        sys.exit(1)
    else:
        logger.info("file_found", file=ACCOUNTS_FILE)

    logger.info("working_directory", path=ROOT_PATH)

    try:
        ENCRYPTION_TYPE = EncryptAlgorithm[args.type]
    except:
        logger.error("Type no exist in EncryptAlgorithm Enum", type=args.type)
        sys.exit(1)

    try:
        ACCESS_TYPE = AccessLevel[args.access_level].name
    except:
        logger.error("Type no exist in AccessLevel Enum", type=args.access_level)
        sys.exit(1)

    manager = AccountManager(ACCOUNTS_FILE)

    if args.list:
        manager.list_accounts()
    elif args.info:
        manager.get_info(args.info)
    elif args.create:
        account_password = getpass.getpass()
        manager.create_account(args.create, account_password, ENCRYPTION_TYPE, ACCESS_TYPE)
    elif args.delete:
        manager.delete_account(args.delete)
    else:
        logger.info("Select any option. Did nothing. Printing help.")
        parser.print_help()
    
    sys.exit(0)