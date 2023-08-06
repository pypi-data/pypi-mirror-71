from __future__ import unicode_literals

from .credentials import Credentials
from .xml import XML
from .exchangelib import ExchangeToMsg
from .toolbox import Toolbox
from .setup_gui import CredentialsGUI, EmailGUI, SQLServerGUI

import os
import pkg_resources

__package_name__ = 'KGlobal'
__author__ = 'Kevin Russell'
__version__ = "1.4.5"
__description__ = '''File, encryption, SQL, XML, and etc...'''
__url__ = 'https://github.com/KLRussell/Python_KGlobal_Package'

__all__ = [
    "Toolbox",
    "Credentials",
    "ExchangeToMsg",
    "XML",
    "CredentialsGUI",
    "EmailGUI",
    "SQLServerGUI",
    "default_key_dir"
]


def default_key_dir():
    if isinstance(__path__, list):
        path = __path__[0]
    else:
        path = __path__

    return os.path.join(path, "Keys")
