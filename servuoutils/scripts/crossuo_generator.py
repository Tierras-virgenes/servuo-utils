import os
import sys
import pathlib

import signal

import argparse

from servuoutils.crossuo import Client

import structlog
logger = structlog.get_logger()

# Global variables
parser = None
args = None

WORKING_DIRECTORY = pathlib.Path().absolute()
ACCOUNT_NAME = "username"
PASSWORD = "password"
BOOL_AUTO_LOGIN = False
BOOL_REMEMBER = False
SERVER_IP_PORT = False
SELECT_THE_ABYSS = False
SELECT_ASMUT = False
SELECT_CRYPT = False

help_description = 'In example: python -m servuoutils.scripts.crossuo_generator -u "testuser" -p "pass" -l -r -o $PWD'
################################################################################
# Functions ####################################################################
################################################################################
def signal_handler(sig, frame):
    logger.info("Signal", sig=sig)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Helper to generate crossuo cfgs. " + help_description,
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-u','--username', help='List update accounts', type=str, metavar='username')
    parser.add_argument('-p','--password', help='Password to add to the config. Warning: It is not going to be encrypt, use raw file.', type=str, metavar='password')
    parser.add_argument('-l','--auto_login', help='Bool to remember or not the auto loging', default=BOOL_AUTO_LOGIN, action='store_true')
    parser.add_argument('-r','--remember', help='Bool to remember or not the password', default=BOOL_REMEMBER, action='store_true')
    parser.add_argument('-i','--ip_server', help='The IP server', default=SERVER_IP_PORT, type=str, metavar='ip_server')
    parser.add_argument('-o','--output', help='The output path', default=WORKING_DIRECTORY, type=str, metavar='path')

    args = parser.parse_args()

    if not args.username:
        logger.error("Username is mandatory")
        parser.print_help()
        sys.exit(1)

    client = Client()

    ACCOUNT_NAME = args.username
    PASSWORD = args.password
    BOOL_AUTO_LOGIN = args.auto_login
    BOOL_REMEMBER = args.remember
    SERVER_IP_PORT = args.ip_server
    SELECT_THE_ABYSS = False
    SELECT_ASMUT = False
    SELECT_CRYPT = False

    client.generate(uopath=WORKING_DIRECTORY, 
                username=ACCOUNT_NAME, 
                password=PASSWORD, 
                server_ip_port = SERVER_IP_PORT,
                custom_path = pathlib.Path().absolute(),
                bool_auto_login = BOOL_AUTO_LOGIN, 
                bool_remember = BOOL_REMEMBER,
                select_the_abyss = SELECT_THE_ABYSS, 
                select_asmut = SELECT_ASMUT, 
                select_crypt = SELECT_CRYPT)
    sys.exit(0)