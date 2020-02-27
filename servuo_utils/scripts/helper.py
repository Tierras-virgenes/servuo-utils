import os
import sys

import signal

import argparse
import shutil
import pathlib

from servuo_utils.servuo_helper import ServUOHelper

import structlog
logger = structlog.get_logger()

# Global variables
parser = None
args = None

ROOT_PATH = pathlib.Path().absolute()

################################################################################
# Functions ####################################################################
################################################################################
def signal_handler(sig, frame):
    logger.info("Signal", sig=sig)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="Helper to manage server data. This helps to use a control version with configuration files, update the submodules (ServUO and crossuo) without lost the files. Also it can backup file saves and configurations to easy porting the server.",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-b','--backup', help='Generate a timestamped copy of the server data. This include save binaries, configuration, and spawns', default="", action='store_true')

    parser.add_argument('-r','--restore', help='Restore a timestamped copy of the server data. This include Save binaries, configuration, and spawns', default="", type=str, metavar='path')

    parser.add_argument('-c','--check', help='Check than required resources are properly installed in Default path. You can provide other path if you want.', default="", action='store_true')

    parser.add_argument('-l','--load', help='Update server files. Copy from repository to server folders. Warning, all changes in server files are override', default="", action='store_true')

    parser.add_argument('-s','--save', help='Update repository files. Copy current server folders to repository. Git will detect changes from last commits, you can discard or commit them.', default="", action='store_true')

    parser.add_argument('-w','--working_directory', help='Set up working directory', default=ROOT_PATH, type=str, metavar='path')

    parser.add_argument('-o','--on', help='EXPERIMENTAL: This command DO NOT redirect stdin and stdout properly. Start running the server from default path', default="", action='store_true')

    args = parser.parse_args()

    if args.working_directory:
        ROOT_PATH = args.working_directory

    logger.info("working_directory", path=ROOT_PATH)

    helper = ServUOHelper(ROOT_PATH)

    if args.load:
        helper.update_server_files()
    elif args.save:
        helper.update_repository_files()
    elif args.check:
        helper.check_resources()
    elif args.backup:
        helper.backup()
    elif args.restore:
        helper.restore(args.restore)
    elif args.on:
        helper.start_server()
    else:
        logger.info("Select any option. Did nothing. Printing help.")
        parser.print_help()
    
    sys.exit(0)
