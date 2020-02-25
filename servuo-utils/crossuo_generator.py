import os
import sys
import pathlib

import signal

import argparse

import structlog
logger = structlog.get_logger()

# Global variables
parser = None
args = None

WORKING_DIRECTORY = pathlib.Path().absolute()
ACCOUNT_NAME = 'user'
PASSWORD = 'user'
BOOL_AUTO_LOGIN = False
BOOL_REMEMBER = False
SELECT_THE_ABYSS = False
SELECT_ASMUT = False
SELECT_CRYPT = False
CUSTOM_PATH = '../../../../resources/2D'
SERVER_IP_PORT = '127.0.0.1,2593'
CLIENT_VERSION = '7.0.45.0'

help_description = """\n\nThis is a script to generate a basic configuration, in example:\n
AcctID=${ACCOUNT_NAME}
AcctPassword=${ACCOUNT_PASSWORD}
RememberAcctPW=no
AutoLogin=no
TheAbyss=no
Asmut=no
Crypt=no
CustomPath=${RESOURCES_PATH}
LoginServer=127.0.0.1,2593
ClientVersion=7.0.45.0
"""

################################################################################
# Functions ####################################################################
################################################################################
def signal_handler(sig, frame):
    logger.info("Signal", sig=sig)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Helper to generate crossuo cfgs." + help_description,
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

    PASSWORD = args.password
    BOOL_AUTO_LOGIN = args.auto_login
    BOOL_REMEMBER = args.remember
    SERVER_IP_PORT = args.ip_server

    logger.info("Generating configuration", username=ACCOUNT_NAME,
                                            password=PASSWORD,
                                            auto_login=BOOL_AUTO_LOGIN,
                                            remember=BOOL_REMEMBER,
                                            abyss=SELECT_THE_ABYSS,
                                            asmut=SELECT_ASMUT,
                                            crypt=SELECT_CRYPT,
                                            resources_path=CUSTOM_PATH,
                                            server_ip=SERVER_IP_PORT,
                                            client_version=CLIENT_VERSION,
                                            output_path=WORKING_DIRECTORY
    )
    sys.exit(0)