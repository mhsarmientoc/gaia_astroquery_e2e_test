"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""
from pathlib import Path
from astropy import config as _config

properties_file = Path(__file__).parent / "../target/properties"
credentials_file = Path(__file__).parent / "../target/pwd"

config_dict = {}
credentials = {}

# Read properties file
with open(properties_file, 'r') as pf:
    for line in pf:
        line = line.strip()
        if line:
            key, value = line.split('=')
            config_dict[key] = value

# Read Credentials File
with open(properties_file, 'r') as pf:
    for line in pf:
        line = line.strip()
        if line:
            key, value = line.split('=')
            credentials[key] = value


class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `astroquery_tests`.
    """

    DATALINK_URL = config_dict['DATALINK_URL']
    HOST_URL = config_dict['HOST_URL']
    TAP_URL = config_dict['TAP_URL']
    ENV_SELECTED = config_dict['CURRENT_ENVIRONMENT']
    TIME_OUT = config_dict['TIME_OUT']
    RESET_TEST = config_dict['RESET_TEST']
    TAP_LOGIN = config_dict['TAP_LOGIN']
    TIMEOUT = config_dict['TIMEOUT']

    CURRENT_HOST = _config.ConfigItem(HOST_URL, "Current host for the e2e test")
    CURRENT_TAP_URL = _config.ConfigItem(TAP_URL, "Current tap url for the env selected")
    CURRENT_DATALINK_URL = _config.ConfigItem(DATALINK_URL, "Current datalink url for the e2e test")
    CURRENT_ENV = _config.ConfigItem(ENV_SELECTED, "Active env for the e2e tests")
    IS_RESET_TEST = _config.ConfigItem(RESET_TEST, "True if the e2e needs to start the whole set")
    CURRENT_TIME_OUT = _config.ConfigItem(TIME_OUT, "Time out until decided to declare the test failed. Sleeping time "
                                                    "after tap upload queries ")
    CURRENT_TAP_LOGIN = _config.ConfigItem(TAP_LOGIN, "Format of url to do login into the current environment")


conf = Conf()


class Credentials:
    USERNAME = credentials['username']
    PASSWORD = credentials['password']


userCredentials = Credentials()

__all__ = ['Conf', 'conf', 'userCredentials', 'Credentials']
