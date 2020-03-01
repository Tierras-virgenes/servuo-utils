import os
import sys
import subprocess

import shutil
import pathlib

import time
import datetime

import tarfile
import errno

from distutils.dir_util import copy_tree
from checksumdir import dirhash

import structlog
logger = structlog.get_logger()


class ServUOHelper(): 
    """
    ServUO Account manager helper

    This class allows to manage accounts.xml easily with the server offline.
    """
    def __init__(self, working_directory):
        self._working_directory = working_directory
        
        self._server_path = os.path.join(self._working_directory, "submodules", "ServUO")
        self._repository_path = os.path.join(self._working_directory, "resources", "tv")
        self._backup_path = os.path.join(self._working_directory, "backups")
        self._resources_path = os.path.join("resources", "2D")

        self._folder_server_list = ["Config"]
        self._backup_folder_list = ["Config", "Saves", "Spawns"]
        self._hash_md5_resources = "93945c306b645459c63adddc299e3760"

        return

    def _recursive_copy(self, src, dst):
        """
        Copy a folder tree overriding destination

        TODO make static

        Notes
        -----
        working directory stay the same.
        """
        working_directory = os.getcwd()
        os.chdir(src)
        for item in os.listdir():
            if os.path.isfile(item):
                shutil.copy(item, dst)
                
            elif os.path.isdir(item):
                new_dst = os.path.join(dst, item)
                os.makedirs(new_dst, exist_ok=True)
                self._recursive_copy(os.path.abspath(item), new_dst)

        # Restore the original working directory
        os.chdir(working_directory)
        return

    def _copy_server_folders(self, src, dst):
        """
        Copy all folders in the SERVER_LIST
        """
        for folder in self._folder_server_list:
            file_src = os.path.join(src, folder)
            file_dst = os.path.join(dst, folder)
            logger.info("copying", file_src=file_src, file_dest=file_dst)
            self._recursive_copy(file_src, file_dst)
        return

    def check_resources(self):
        """
        Check than required resources are properly installed in Default path. 

        * Check if exist default resources 2D path
        * Check if checksum is the same

        Notes
        -----
        You can provide other path if you want.
        """
        if not os.path.exists(self._resources_path):
            logger.error("Resources default path no exists", path=self._resources_path)
            return

        logger.info("Calculating resources MD5", path=self._resources_path)
        md5hash = dirhash(self._resources_path, 'md5')
        if not self._hash_md5_resources == md5hash:
            logger.error("Bad MD5 checksum for resources", hash=md5hash, expected=self._hash_md5_resources)
            return
            
        logger.info("Resources path looks OK", hash=md5hash)
        return

    def update_server_files(self):
        """
        Update repository files. Copy current server folders to repository.
        """
        src = self._repository_path
        dest = self._server_path
        logger.info("update_server_files", src=src, dest=dest)
        self._copy_server_folders(src, dest)
        return
        
    def update_repository_files(self):
        """
        Update server files. Copy from repository to server folders.
        """
        src = self._server_path
        dest = self._repository_path
        logger.info("update_repository_files", src=src, dest=dest)
        self._copy_server_folders(src, dest)
        return

    def backup(self):
        """
        Generate backup file with timestamp name

        * The saved folders are stored at: self._backup_folder_list
        * A tar file will be generated.
        * The name contain the backup timestamp.
        """
        timestamp_name = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ".tar"
        output_file = os.path.join(self._backup_path, timestamp_name)
        
        logger.info("Generating backup tar file", file=output_file)

        with tarfile.open(output_file, 'w') as tar:
            for folder in self._backup_folder_list:
                current_folder = os.path.join(self._server_path, folder)
                logger.info("Adding folder", folder=current_folder)
                tar.add(current_folder, arcname=folder)
        
        time.sleep(0.001)
        return

    def restore(self, backup_file):
        """
        Restore give backup file in server path
        """
        logger.info("Restoring backup file", path=backup_file)

        if not os.path.isfile(backup_file):
            logger.error("Path no exist", path=backup_file)
            return False

        logger.info("Extracting at server path", path=self._server_path)
        with tarfile.open(backup_file, 'r') as tar:
            tar.extractall(self._server_path)
        return True

    def start_server(self):
        """
        Start running the server
        """
        logger.info("Starting server")
        working_directory = os.getcwd()
        os.chdir(self._server_path)

        if sys.platform.startswith('linux'):
            logger.info("Detected GNU/Linux platform")
            p = subprocess.Popen('make', stdout=subprocess.PIPE)
            while p.poll() is None:
                log = p.stdout.readline() # This blocks until it receives a newline.
                print(log.decode())
        elif sys.platform.startswith('win32'):
            logger.info("Detected windows platform")
        elif sys.platform.startswith('darwin'):
            logger.info("Detected MacOS platform")
        else:
            logger.info("Not valid platform")

        # Restore the original working directory
        os.chdir(working_directory)
        return