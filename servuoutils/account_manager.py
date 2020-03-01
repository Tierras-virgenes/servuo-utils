from enum import Enum
from collections import OrderedDict

import hashlib
import xmltodict

import structlog
logger = structlog.get_logger()

class EncryptAlgorithm(Enum):
    """
    Enum to set up different encryptions
    """
    NONE = 0            # None
    Crypt = 1           # MD5
    NewCrypt = 2        # SHA1
    NewSecureCrypt = 3  # SHA512

class AccessLevel(Enum):
    """
    Enum to set up different access levels
    """
    Player = 0          
    VIP = 1
    Counselor = 2
    Decorator = 3
    Spawner = 4
    GameMaster = 5
    Seer = 6
    Administrator = 7
    Developer = 8
    CoOwner = 9
    Owner = 10

class AccountManager(): 
    """
    ServUO Account manager helper

    This class allows to manage accounts.xml easily with the server offline.
    """
    def __init__(self, account_file):
        self._accounts_file = account_file
        return

    def generate_password(self, username, password, type):
        """
        Generate a password using username + password bytes as input.

        This function use both because implementation in ServUO
        """
        encoded = str(username + password).encode('ascii')
        key_sha = encoded
        if type == EncryptAlgorithm.Crypt:
            logger.info("Generating MD5 - Crypt password")
            key_sha = hashlib.md5(encoded).hexdigest().upper()
        elif type == EncryptAlgorithm.NewCrypt:
            logger.info("Generating SHA1 - NewCrypt password")
            key_sha = hashlib.sha1(encoded).hexdigest().upper()
        elif type == EncryptAlgorithm.NewSecureCrypt:
            logger.info("Generating SHA512 - NewSecureCrypt password")
            key_sha = hashlib.sha512(encoded).hexdigest().upper()
        else:
            logger.info("Generating unsafe password")
        processed_pass = '-'.join([key_sha[i:i+2] for i in range(0, len(key_sha), 2)])
        return processed_pass

    def create_account_node(self, username, password, level='Player'):
        logger.info("creating_account", username=username, access_level=level)
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

    def list_accounts(self):
        """
        Print a list all players in server
        """
        with open(self._accounts_file, "r") as fd:
            doc = xmltodict.parse(fd.read())
            accounts = doc['accounts']['account']
            for index, account in enumerate(accounts):
                access_level = account.get('accessLevel', 'Player') 
                logger.info("Account {:04d}".format(index), username=account['username'], type=access_level)
        return

    def get_info(self, account_name):
        """
        Print the info from a player
        """
        with open(self._accounts_file, "r") as fd:
            doc = xmltodict.parse(fd.read())
            accounts = doc['accounts']['account']
            user = self._get_value_from_list(accounts, account_name)

            if not user:
                logger.error("account_not_found", account_name=account_name)
                return False

            logger.info("account_found", lastLogin=user['lastLogin'], created=user['created'], totalGameTime=user['totalGameTime'], totalCurrency=user['totalCurrency'], sovereigns=user['sovereigns'])
        return True

    def create_account(self, account_name, account_password, encrypt_type, level):
        """
        Create an account if not exists
        """
        with open(self._accounts_file, "r") as fd:
            doc = xmltodict.parse(fd.read())
            accounts = doc['accounts']['account']
            user = self._get_value_from_list(accounts, account_name)

            if user:
                logger.error("account_already_exists", account_name=account_name)
                return False

            password = generate_password(account_name, account_password, encrypt_type)
            account = create_account_node(account_name, password, level)
            accounts.append(account)

        with open(self._accounts_file, "w") as fd2:
            fd2.write(xmltodict.unparse(doc))
        return True

    def delete_account(self, account_name):
        """
        Delete an account if exists
        """
        with open(self._accounts_file, "r") as fd:
            doc = xmltodict.parse(fd.read())
            accounts = doc['accounts']['account']
            user = self._get_value_from_list(accounts, account_name)

            if not user:
                logger.error("account_not_found", account_name=account_name)
                return False

            logger.info("deleting_account", account_name=account_name)
            self._del_value_from_list(accounts, account_name)

        with open(self._accounts_file, "w") as fd2:
            fd2.write(xmltodict.unparse(doc, pretty = True))
        return True

    def _get_value_from_list(self, target_list, key):
        """
        Get a key value from a list

        Returns
        -------
        value: None if not found
        """
        return next((item for item in target_list if item["username"] == key), None)

    def _del_value_from_list(self, target_list, key):
        """
        Delete a key if exist in the list
        """
        for index, item in enumerate(target_list):
            if item["username"] == key:
                target_list.pop(index)
        return
