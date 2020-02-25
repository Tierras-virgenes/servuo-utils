import os
import sys

import signal

import argparse

import pathlib
import hashlib 

import xmltodict
from collections import OrderedDict

import structlog
logger = structlog.get_logger()

# Global variables
parser = None
args = None

ROOT_PATH = pathlib.Path().absolute()
ACCOUNTS_FILE = os.path.join(ROOT_PATH, "submodules", "ServUO", "Saves", "Accounts", "accounts.xml")
TEST_FILE = os.path.join(ROOT_PATH, "accounts.xml")

################################################################################
# Functions ####################################################################
################################################################################
def signal_handler(sig, frame):
    logger.info("Signal", sig=sig)

def get_value_from_list(target_list, key):
    """
    Get a key value from a list

    Returns
    -------
    value: None if not found
    """
    return next((item for item in target_list if item["username"] == key), None)

def del_value_from_list(target_list, key):
    """
    Delete a key if exist in the list
    """
    for index, item in enumerate(target_list):
        if item["username"] == key:
            target_list.pop(index)
    return

def create_account_node(username, password, level='Player'):
    node = OrderedDict([('username', username), 
                        ('newSecureCryptPassword', password), 
                        ('accessLevel', level), 
                        ('created', ''),
                        ('lastLogin', ''),
                        ('chars', None),
                        ('totalGameTime', 'PT0S'),
                        ('totalCurrency', '0'),
                        ('sovereigns', '0'),
                        ])
    return node

def list_accounts():
    """
    Print a list all players in server
    """
    with open(ACCOUNTS_FILE, "r") as fd:
        doc = xmltodict.parse(fd.read())
        accounts = doc['accounts']['account']
        for index, account in enumerate(accounts):
            access_level = account.get('accessLevel', 'Player') 
            logger.info("Account {:04d}".format(index), username=account['username'], type=access_level)
    return

def get_info(account_name):
    """
    Print the info from a player
    """
    with open(ACCOUNTS_FILE, "r") as fd:
        doc = xmltodict.parse(fd.read())
        accounts = doc['accounts']['account']
        user = get_value_from_list(accounts, account_name)

        if not user:
            logger.error("Account not found", account_name=account_name)
            return False

        logger.info("Account found", lastLogin=user['lastLogin'], created=user['created'], totalGameTime=user['totalGameTime'], totalCurrency=user['totalCurrency'], sovereigns=user['sovereigns'])
    return True

def create_account(account_name):
    with open(ACCOUNTS_FILE, "r") as fd:
        doc = xmltodict.parse(fd.read())
        accounts = doc['accounts']['account']
        user = get_value_from_list(accounts, account_name)

        if user:
            logger.error("Account already exists", account_name=account_name)
            return False

        account = create_account_node(account_name, "pass")
        accounts.append(account)

    with open(ACCOUNTS_FILE, "w") as fd2:
        fd2.write(xmltodict.unparse(doc))
    return True

def delete_account(account_name):
    with open(ACCOUNTS_FILE, "r") as fd:
        doc = xmltodict.parse(fd.read())
        accounts = doc['accounts']['account']
        user = get_value_from_list(accounts, account_name)

        if not user:
            logger.error("Account not found", account_name=account_name)
            return False

        logger.info("Deleting account", account_name=account_name)
        del_value_from_list(accounts, account_name)

    with open(ACCOUNTS_FILE, "w") as fd2:
        fd2.write(xmltodict.unparse(doc))
    return True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Helper to manage server accounts.",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-l','--list', help='List update accounts', default="", action='store_true')
    parser.add_argument('-i','--info', help='Get info from an account', default="", type=str, metavar='account_name')
    parser.add_argument('-c','--create', help='Create a game account if no exists', default="", type=str, metavar='account_name')
    parser.add_argument('-t','--type', help='Set up another encryption type', default="", type=str, metavar='path')
    parser.add_argument('-d','--delete', help='Delete an account if exist.', default="", type=str, metavar='account_name')
    

    args = parser.parse_args()

    if not os.path.isfile(ACCOUNTS_FILE):
        logger.error("File no exist", file=ACCOUNTS_FILE)
        sys.exit(1)

    if args.list:
        list_accounts()
    elif args.info:
        get_info(args.info)
    elif args.create:
        create_account(args.create)
    elif args.delete:
        delete_account(args.delete)
    else:
        logger.info("Select any option. Did nothing. Printing help.")
        parser.print_help()
    
    sys.exit(0)