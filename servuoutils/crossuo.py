import pathlib

import structlog
logger = structlog.get_logger()

class Client(): 
    """
    ServUO client cfg generator

    This class generate a valid configuration for CrossUO.

    In example:
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
    def __init__(self):
        self._account_name = 'user'
        self._password = 'user'
        self._custom_path = pathlib.Path().absolute()
        self._bool_auto_login = False
        self._bool_remember = False
        self._select_the_abyss = False
        self._select_asmut = False
        self._select_crypt = False
        
        self._server_ip_port = '127.0.0.1,2593'
        self._client_version = '7.0.45.0'
        return

    def generate(self, uopath, username, password, 
                server_ip_port = '127.0.0.1,2593',
                custom_path = pathlib.Path().absolute(),
                bool_auto_login = False, bool_remember = False,
                select_the_abyss = False, select_asmut = False, select_crypt = False):
        """
        Generate a config using username, password and other configuration parameters
        """
        self._uopath = uopath
        
        self._account_name = username
        self._password = password
        self._server_ip_port = server_ip_port
        self._custom_path = custom_path

        self._bool_auto_login = bool_auto_login
        self._bool_remember = bool_remember

        self._select_the_abyss = select_the_abyss
        self._select_asmut = select_asmut
        self._select_crypt = select_crypt
        
        self._client_version = '7.0.45.0'

        logger.info("generating_cfg", uopath = self._uopath,
            username = self._account_name,
            ipport=self._server_ip_port,
            custom_path = self._custom_path,
            auto_login=self._bool_auto_login,
            remember=self._bool_remember,
            abyss=self._select_the_abyss,
            asmut=self._select_asmut,
            crypt=self._select_crypt,
            client=self._client_version
        )
        return