import os
import pathlib

from jinja2 import Template

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
        self._uopath = pathlib.Path().absolute()
        self._bool_auto_login = False
        self._bool_remember = False
        self._select_the_abyss = False
        self._select_asmut = False
        self._select_crypt = False
        
        self._server_ip_port = '127.0.0.1,2593'
        self._client_version = '7.0.45.0'

        self._tm = Template(
        "AcctID={{ username }}" + "\n" +
        "AcctPassword={{ password }}" + "\n" +
        "RememberAcctPW={% if remember %}yes{% else %}no{% endif %}" + "\n" +
        "AutoLogin={% if auto_login %}yes{% else %}no{% endif %}" + "\n" +
        "TheAbyss={% if abyss %}yes{% else %}no{% endif %}" + "\n" +
        "Asmut={% if asmut %}yes{% else %}no{% endif %}" + "\n" +
        "Crypt={% if crypt %}yes{% else %}no{% endif %}" + "\n" +
        "CustomPath={{ uopath }}" + "\n" +
        "LoginServer={{ ipport }}" + "\n" +
        "ClientVersion={{ client }}" + "\n"
        )
        return

    def generate(self, path, username, password, 
                server_ip_port = '127.0.0.1,2593',
                uopath = pathlib.Path().absolute(),
                bool_auto_login = False, bool_remember = False,
                select_the_abyss = False, select_asmut = False, select_crypt = False):
        """
        Generate a config using username, password and other configuration parameters
        """
        self._path = path
        
        self._account_name = username
        self._password = password
        self._server_ip_port = server_ip_port
        self._uopath = uopath

        self._bool_auto_login = bool_auto_login
        self._bool_remember = bool_remember

        self._select_the_abyss = select_the_abyss
        self._select_asmut = select_asmut
        self._select_crypt = select_crypt
        
        self._client_version = '7.0.45.0'

        logger.info("generating_cfg", path = self._path,
            username = self._account_name,
            ipport=self._server_ip_port,
            uopath = self._uopath,
            auto_login=self._bool_auto_login,
            remember=self._bool_remember,
            abyss=self._select_the_abyss,
            asmut=self._select_asmut,
            crypt=self._select_crypt,
            client=self._client_version
        )

        msg = self._tm.render(username = self._account_name,
            password = self._password,
            ipport = self._server_ip_port,
            uopath = self._uopath,
            auto_login = self._bool_auto_login,
            remember = self._bool_remember,
            abyss = self._select_the_abyss,
            asmut = self._select_asmut,
            crypt = self._select_crypt,
            client = self._client_version
        )
        filename = os.path.join(self._path, "crossuo.cfg")
        with open(filename, "w") as fd:
            fd.write(msg)
        return True