"""
@author: ESDC team
@contact: esdc_gaia_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 05 Sep. 2020
"""
import os
import shutil
import logging as log
from pathlib import Path

from astropy import config as _config


class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `astroquery_tests`.
    """
    config_dict = {}

    # Get current root directory
    currentDirectory = os.getcwd()

    if 'target' in currentDirectory:
        properties_file = Path(__file__).parents[2].joinpath("target/properties", "properties")
    else:
        # Setup paths for the whole project
        properties_file = Path(__file__).parents[1].joinpath("target/properties", "properties")

    # Read properties file
    with open(properties_file, 'r') as pf:
        for line in pf:
            line = line.strip()
            if line:
                print(line)
                if "=" in line:
                    key, value = line.split('=')
                    config_dict[key] = value

    DATALINK_URL = config_dict['DATALINK_URL']
    HOST_URL = config_dict['HOST_URL']
    TAP_URL = config_dict['TAP_URL']
    ENV_SELECTED = config_dict['CURRENT_ENVIRONMENT']
    RESET_TEST = config_dict['RESET_TEST']
    TAP_LOGIN = config_dict['TAP_LOGIN']
    TIME_OUT = config_dict['TIME_OUT']
    ASTROQUERY_VERSION = config_dict['ASTROQUERY_VERSION']
    GAIA_DATA_RELEASE = config_dict['GAIA_DATA_RELEASE']
    DB_SCHEMA_NAME = config_dict['DB_SCHEMA_NAME']
    GAIA_SOURCE_DB_NAME = config_dict['GAIA_SOURCE_DB_NAME']
    LOG_LEVEL = config_dict['LOG_LEVEL']
    DATA_FORMAT = config_dict['DATA_FORMAT']
    DATA_STRUCTURE = config_dict['DATA_STRUCTURE']
    # ---------------------------------------------------------
    CURRENT_HOST = _config.ConfigItem(HOST_URL, "Current host for the e2e test")
    CURRENT_TAP_URL = _config.ConfigItem(TAP_URL, "Current tap url for the env selected")
    CURRENT_DATALINK_URL = _config.ConfigItem(DATALINK_URL, "Current datalink url for the e2e test")
    CURRENT_ENV = _config.ConfigItem(ENV_SELECTED, "Active env for the e2e tests")
    IS_RESET_TEST = _config.ConfigItem(RESET_TEST, "True if the e2e needs to start the whole set")
    CURRENT_TIME_OUT = _config.ConfigItem(TIME_OUT, "Time out until decided to declare the test failed. Sleeping time "
                                                    "after tap upload queries ")
    CURRENT_TAP_LOGIN = _config.ConfigItem(TAP_LOGIN, "Format of url to do login into the current environment")
    CURRENT_ASTROQUERY_VERSION = _config.ConfigItem(ASTROQUERY_VERSION, "Version of Astroquery against which we are "
                                                                        "running this e2e tests")
    CURRENT_GAIA_DATA_RELEASE = _config.ConfigItem(GAIA_DATA_RELEASE, "Gaia Data Release used for the e2e tests")

    DB_SCHEMA_NAME = _config.ConfigItem(DB_SCHEMA_NAME, "Gaia Data Release used for the e2e tests")
    GAIA_SOURCE_DB_NAME = _config.ConfigItem(GAIA_SOURCE_DB_NAME, "Gaia Data Release used for the e2e tests")
    CURRENT_LOG_LEVEL = _config.ConfigItem(LOG_LEVEL, "Log level selected. As default logs are set to DEBUG")

    CURRENT_DATA_FORMAT = _config.ConfigItem(DATA_FORMAT, "Possible values for 'DATA_FORMAT' can be votable | fits | "
                                                          "csv")
    CURRENT_DATA_STRUCTURE = _config.ConfigItem(DATA_STRUCTURE,
                                                "Possible values for 'DATA_STRUCTURE' can be Individual "
                                                "| Combined | Raw")


# __end_of_class_Conf

conf = Conf()


class Credentials:
    """
        This class store the credentials read from file once that project has been compiled with maven,
        and the correct values replaced in the file during the compilation time.
    """

    credentials = {}
    credentials_file = None

    # Get current root directory
    currentDirectory = os.getcwd()

    if 'target' in currentDirectory:
        credentials_file = Path(__file__).parents[1].joinpath("target/properties", "pwd")
    else:
        credentials_file = Path(__file__).parents[1].joinpath("target/properties", "pwd")

    # Read Credentials File
    with open(credentials_file, 'r') as pf:
        for line in pf:
            line = line.strip()
            if line:
                print(line)
                if "=" in line:
                    key, value = line.split('=')
                    credentials[key] = value

    USERNAME = credentials['username']
    PASSWORD = credentials['password']


# __end_of_class_Credentials

credentials = Credentials()


def clean_directory(path):
    """
    Clean output directories prior starting with the e2e campaign
    :param path: path in which are stored the files to remove
    :return:
    """
    if Path(path).is_dir():
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        log.debug(f'path: {path} is already empty. Nothing to do here!')


# __end_of_clean_directory

def clean_files(path, extension):
    """
    aux method to remove files with a specific extension

    :param path: path to the directory from which we want to remove the files
    :param extension: extension of the files to be removed
    :return:
    """
    files_in_directory = os.listdir(path)
    filtered_files = [file for file in files_in_directory if file.endswith(extension)]
    for file in filtered_files:
        path_to_file = os.path.join(path, file)
        os.remove(path_to_file)


# __end_of_clean_files


class ProjectPaths:
    """
        This class prepared the paths for the project depending on the current environment
    """

    # Get current root directory
    currentDirectory = os.getcwd()

    if 'target' in currentDirectory:

        # we are running code from the deployed library
        folder_in = Path(__file__).parent / '../test_report/toml/'
        folder_out = Path(__file__).parent / '../test_report/html/'
        path2_example_tb_4_onthefly = Path(__file__).parent / './resources/test_table_4_on_the_fly_query.vot'
        path2_example_table_for_tests = Path(__file__).parent / './resources/1601309792192D-result.vot'
        path2_Datalink_test_products = Path(__file__).parent / f'./resources/DataLink_Products_{conf.CURRENT_ENV}'
        path2_TestDescription = Path(__file__).parent / "./main/toml_test_description/TestDescription.toml"
        path2_E2ETestResults = Path(__file__).parent / '../test_report/toml/E2ETestResults.toml'
        path2_Datalink_test_products_outdir = Path(
            __file__).parent / f'./resources/DataLink_Products_{conf.CURRENT_ENV}/outdir'
        path2_to_logs = Path(__file__).parent / '../logs/'

    else:

        folder_in = Path(__file__).parent / '../test_report/toml/'
        folder_out = Path(__file__).parent / '../test_report/html/'
        path2_example_tb_4_onthefly = Path(__file__).parent / './main/resources/test_table_4_on_the_fly_query.vot'
        path2_example_table_for_tests = Path(__file__).parent / './main/resources/1601309792192D-result.vot'
        path2_Datalink_test_products = Path(__file__).parent / f'./main/resources/DataLink_Products_{conf.CURRENT_ENV}'
        path2_TestDescription = Path(__file__).parent / './main/toml_test_description/TestDescription.toml'
        path2_E2ETestResults = Path(__file__).parent / '../test_report/toml/E2ETestResults.toml'
        path2_Datalink_test_products_outdir = Path(
            __file__).parent / f'./main/resources/DataLink_Products_{conf.CURRENT_ENV}/outdir'
        path2_to_logs = Path(__file__).parent / '../logs/'

    # clean output directory before starting the tests
    clean_directory(f'{path2_Datalink_test_products_outdir}/individual_vot')
    clean_directory(f'{path2_Datalink_test_products_outdir}/individual_fits')
    clean_directory(f'{path2_Datalink_test_products_outdir}/individual_csv')
    clean_directory(f'{path2_Datalink_test_products_outdir}/combined_vot')
    clean_directory(f'{path2_Datalink_test_products_outdir}/combined_fits')
    clean_directory(f'{path2_Datalink_test_products_outdir}/combined_csv')
    clean_directory(f'{path2_Datalink_test_products_outdir}/raw_vot')
    clean_directory(f'{path2_Datalink_test_products_outdir}/raw_fits')
    clean_directory(f'{path2_Datalink_test_products_outdir}/raw_csv')

    # clean html reports from previous tests

    clean_files(f'{folder_out}', f'.html')


# __end_of_class_ProjectPaths

paths = ProjectPaths()

__all__ = ['Conf', 'conf', 'credentials', 'Credentials', 'paths', 'ProjectPaths']
